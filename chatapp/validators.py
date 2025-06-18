# your_app/validators.py

from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import re
from django.contrib.auth import get_user_model

User = get_user_model()

def is_valid_username(username):
    """
    Checks if the username is valid format and unique.
    - Only letters, numbers, underscores
    - Minimum 3 characters
    """
    if not username:
        return False, "Username is required"
    
    if not re.match(r'^[a-zA-Z0-9_]{3,}$', username):
        return False, "Username must be at least 3 characters and alphanumeric"

    if User.objects.filter(username=username).exists():
        return False, "Username already exists"
    
    return True, None

def is_valid_email(email):
    """
    Checks if the email is valid format and unique.
    """
    if not email:
        return False, "Email is required"

    try:
        validate_email(email)
    except DjangoValidationError:
        return False, "Invalid email format"
    
    if User.objects.filter(email=email).exists():
        return False, "Email already exists"
    
    return True, None
