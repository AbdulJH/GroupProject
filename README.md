# PDF2Quiz : AI-powered Notes-to-Quiz generator

A web application that converts PDF study materials into interactive quizzes.

## What It Does

- Users upload PDF documents (notes, textbooks, study guides)
- The app extracts text and generates true/false quiz questions using AI
- Users take the quiz and submit answers
- Results are saved to track progress over time

## Tech Stack

**Backend:** FastAPI, Python, PostgreSQL
**Frontend:** HTML, CSS, JavaScript, Jinja2 templates
**Infrastructure:** Docker, Docker Compose

## Requirements

- Docker Desktop: https://www.docker.com/products/docker-desktop/

## How to Run

1. Clone the repository
```bash
   git clone https://github.com/yourusername/pdf2quiz.git
   cd pdf2quiz
```

2. Start the application

   First time or after making changes:
```bash
   docker-compose up --build
```

   If already built:
```bash
   docker-compose up
```

3. Open your browser and go to:
```
   http://localhost:5001/register
```

4. To stop the application:
```bash
   docker-compose down
```

## Project Structure
```
pdf2quiz/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # Database functions
│   │   ├── models.py        # Data models
│   │   └── routes/
│   │       ├── auth.py      # Login/register routes
│   │       └── pdf.py       # PDF upload and quiz routes
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── static/              # CSS, JavaScript
│   └── templates/           # HTML templates
├── docker-compose.yml
└── README.md
```

## Database Access

To view the database while the app is running:
```bash
docker exec -it groupproject-db-1 psql -U postgres -d ics499db
```

View users table:
```sql
SELECT * FROM users;
```

Exit:
```
\q
```

## Features

### Implemented
- User registration and login
- PDF upload
- Text extraction from PDFs
- Quiz question generation using Gemini
- Quiz taking interface
- Email validation

### Planned
- Score calculation
- Results history
- Leaderboard
- Tutor dashboard
- Custom quiz creation

## Team

- Dagmawite Mamo - Frontend Developer
- Abduljabaar Hussein - Frontend Developer
- Gaoussou Thiam - Backend Developer
- Omar Ahmed - Database

