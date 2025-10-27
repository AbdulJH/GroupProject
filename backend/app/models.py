from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """
    Data model for user registration.
    Validates that all required fields are present and are strings.

    This matches the HTML form fields in register.html:
    - username (from: name="username")
    - email (from: name="email")
    - password (from: name="password")
    - confirm_password (from: name="confirm_password")
    """
    username: str
    email: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    """
    Data model for user login.
    Validates that username and password are provided and are strings.

    This matches the HTML form fields in login.html:
    - username (from: name="username")
    - password (from: name="password")
    """
    username: str
    password: str