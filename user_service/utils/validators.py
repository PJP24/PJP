import re


def is_valid_username(username: str) -> bool:
    return len(username) >= 5


def is_valid_email(email: str):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    return re.match(email_validate_pattern, email)

def is_valid_password(password: str):
    password_validate_pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$"
    return re.match(password_validate_pattern, password)