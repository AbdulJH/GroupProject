import pdfplumber


def file_processor(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = pdf.pages
            text = ""

            for page in pages:
                text += page.extract_text() + '\n'
    
            print(text)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    file_path = input("Enter the file path: ")
    file_processor(file_path)


