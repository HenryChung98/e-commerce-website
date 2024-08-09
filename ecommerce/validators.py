import string
from django.core.exceptions import ValidationError

def contains_uppercase_letter(value):
    for char in value:
        if char.isupper():
            return True
    return False

def contains_lowercase_letter(value):
    for char in value:
        if char.islower():
            return True
    return False

def contains_number(value):
    for char in value:
        if char.isdigit():
            return True
    return False


def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if (
            len(password) < 8 or
            not contains_uppercase_letter(password) or
            not contains_lowercase_letter(password) or
            not contains_number(password) or 
            not contains_special_character(password)
        ):
            raise ValidationError("Your password must contain at least 8 characters.")
        
    def get_help_text(self):
        return "Your password must contain at least 8 characters."





def validate_no_special_characters(value):
    if contains_special_character(value):
        raise ValidationError("special character cannot be included")
