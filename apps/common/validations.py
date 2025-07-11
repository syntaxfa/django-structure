import re


iranian_mobile_regex = r"^09\d{9}$"

def validate_iranian_mobile(mobile: str) -> bool:
    if not re.match(iranian_mobile_regex, mobile):
        return False
    return True


iranian_telephone_pattern = r"^(0[1-9]{2,3})([2-9][0-9]{7})$"

def validate_iranian_telephone(telephone: str) -> bool:
    if not re.match(iranian_telephone_pattern, telephone):
        return False
    return True
