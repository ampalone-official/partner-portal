# app/utils/validators.py
"""
Ampalone Partner Portal - Validation Utilities
Version: 1.0.0
"""

import re


def validate_pan(pan_number: str) -> bool:
    """
    Validate Indian PAN number format
    Format: ABCDE1234F (5 letters, 4 digits, 1 letter)
    """
    if not pan_number:
        return False
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pan_pattern, pan_number.upper()))


def validate_gst(gst_number: str) -> bool:
    """
    Validate Indian GST number format
    Format: 22AAAAA0000A1Z5 (2 digits, 5 letters, 4 digits, 1 letter, 1 alphanumeric, Z, 1 alphanumeric)
    """
    if not gst_number:
        return False
    gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(gst_pattern, gst_number.upper()))


def validate_cin(cin_number: str) -> bool:
    """
    Validate Indian CIN (Corporate Identification Number)
    Format: U72200KA2020PTC134567 (21 characters)
    """
    if not cin_number:
        return False
    cin_pattern = r'^[UPL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$'
    return bool(re.match(cin_pattern, cin_number.upper()))


def validate_ifsc(ifsc_code: str) -> bool:
    """
    Validate Indian IFSC code
    Format: HDFC0001234 (4 letters, 0, 6 digits/letters)
    """
    if not ifsc_code:
        return False
    ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(ifsc_pattern, ifsc_code.upper()))


def validate_phone(phone: str, country_code: str = "IND") -> bool:
    """Validate phone number based on country"""
    if country_code == "IND":
        # Indian phone: 10 digits starting with 6-9
        pattern = r'^[6-9][0-9]{9}$'
        return bool(re.match(pattern, phone))
    else:
        # International: basic validation
        return len(phone) >= 10 and len(phone) <= 15


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""
