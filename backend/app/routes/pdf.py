import pdfplumber
import json
import google.generativeai as genai
from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import save_quiz_result
from app.routes.auth import get_current_user
from app.database import get_quiz_history

# Setup
router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

# Configure Gemini
genai.configure(api_key="#") 

# Storage
CURRENT_QUIZ = None


def extract_text_from_pdf(pdf_file):
    """Extract all text from uploaded PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def generate_quiz_from_text(pdf_text):
    """Use Gemini AI to generate 5 true/false questions from PDF text."""
    prompt = f"""
    Based on the following text, generate exactly 5 true/false questions.
    The questions should test understanding of the key concepts in the text.
    
    Return ONLY a valid JSON array in this exact format (no markdown, no code blocks, no extra text):
    [
      {{"question": "First question here", "answer": true}},
      {{"question": "Second question here", "answer": false}},
      {{"question": "Third question here", "answer": true}},
      {{"question": "Fourth question here", "answer": false}},
      {{"question": "Fifth question here", "answer": true}}
    ]
    
    Text to analyze:
    {pdf_text}
    """
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    try:
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        questions = json.loads(response_text)
        return questions
    except json.JSONDecodeError as e:
        print(f"Error parsing AI response: {e}")
        print(f"Raw response: {response.text}")
        return [
            {"question": "Error generating quiz. Please try again.", "answer": True}
        ]


@router.post("/upload")
async def upload_pdf(request: Request, pdf_file: UploadFile = File(...)):
    """Handle PDF file upload and generate quiz."""
    global CURRENT_QUIZ
    
    # Extract text from PDF
    try:
        pdf_text = extract_text_from_pdf(pdf_file)
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return templates.TemplateResponse(
            "pdf2quizhome.html",
            {"request": request, "error": "Failed to read PDF. Please try another file.", "current_user": get_current_user()}
        )
    
    # Generate quiz questions
    try:
        questions = generate_quiz_from_text(pdf_text)
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return templates.TemplateResponse(
            "pdf2quizhome.html",
            {"request": request, "error": "Failed to generate quiz. Please try again.", "current_user": get_current_user()}
        )
    
    # Store quiz
    CURRENT_QUIZ = questions
    
    # Redirect to quiz page
    return RedirectResponse(url="/quiz", status_code=303)


@router.get("/quiz")
def show_quiz(request: Request):
    """Display quiz questions to the user."""
    global CURRENT_QUIZ
    
    # Check if quiz exists
    if CURRENT_QUIZ is None:
        return RedirectResponse(url="/pdf2quizhome", status_code=303)
    
    # Render quiz page
    return templates.TemplateResponse(
        "quiz_take.html",
        {
            "request": request,
            "questions": CURRENT_QUIZ,
            "current_user": get_current_user()
        }
    )


@router.post("/quiz/submit")
async def submit_quiz(request: Request):
    """
    Handle quiz submission, calculate score, save to database.
    """
    global CURRENT_QUIZ
    
    # Check if quiz exists
    if CURRENT_QUIZ is None:
        return RedirectResponse(url="/pdf2quizhome", status_code=303)
    
    # Get current logged-in user
    username = get_current_user()
    if not username:
        # User not logged in, redirect to login
        return RedirectResponse(url="/login", status_code=303)
    
    # Get form data (user's answers)
    form_data = await request.form()

    
    # Calculate score
    score = 0
    total_questions = len(CURRENT_QUIZ)
    results = []
    
    for i in range(total_questions):
        # Get user's answer for this question
        user_answer_str = form_data.get(f"question_{i}")
        
        if user_answer_str is None:
            continue  # Question not answered (shouldn't happen with required fields)
        
        # Convert string to boolean
        user_answer = (user_answer_str.lower() == "true")
        
        # Get correct answer
        correct_answer = CURRENT_QUIZ[i]["answer"]

        is_correct = (user_answer == correct_answer)
    
        if is_correct:
            score += 1
    
        # Store result for this question
        results.append({
            "question": CURRENT_QUIZ[i]["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })
        
        
    
    # Calculate percentage
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    # Save to database
    save_quiz_result(username, score, total_questions)
    
    # Clear the current quiz
    CURRENT_QUIZ = None
    
    # Show results page with score
    return templates.TemplateResponse(
        "quiz_submitted.html",
        {
            "request": request,
            "score": score,
            "total": total_questions,
            "percentage": round(percentage, 1),
            "current_user": get_current_user(),
            "results": results
        }
    )


@router.get("/quiz/history")
def quiz_history(request: Request):
    """
    Show user's quiz history and average score.
    """
    # Get current logged-in user
    username = get_current_user()
    if not username:
        # Not logged in, redirect to login
        return RedirectResponse(url="/login", status_code=303)
    
    # Get quiz history from database
    history = get_quiz_history(username)
    
    # Render history page
    return templates.TemplateResponse(
        "quiz_history.html",
        {
            "request": request,
            "quizzes": history['quizzes'],
            "average": history['average'],
            "total_quizzes": history['total_quizzes'],
            "current_user": get_current_user()
        }
    )