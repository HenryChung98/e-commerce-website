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

def postal_code(postal_code, country='CA'):
    patterns = {
        'US': r'^\d{5}(?:-\d{4})?$',
        'CA': r'^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$',  # e.g. K1A 0B1
        'UK': r'^([A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2})$',  # e.g. W1A 1AA
        'KR': r'^\d{5}$'  #  12345
    }
    pattern = patterns.get(country)
    if not pattern:
        return False

    return True


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

def validate_no_numbers(value):
    if contains_number(value):
        raise ValidationError("number cannot be included")
    
def validate_postal_code(value):
    if not postal_code(value):
        raise ValueError('Unsupported country code')
    
