import re

def assess_password_strength(password):
    # Check password length
    if len(password) < 8:
        return "Weak - Password is too short"
    
    # Check for common password patterns
    common_patterns = [
        r'(?i)password',
        r'(?i)123456',
        r'(?i)qwerty',
        r'(?i)abcdef',
        r'(?i)p@ssw0rd',
    ]
    for pattern in common_patterns:
        if re.search(pattern, password):
            return "Weak - Password is too common"
    
    # Check for complexity
    if not re.search(r'[a-z]', password):
        return "Weak - Password must contain at least one lowercase letter"
    if not re.search(r'[A-Z]', password):
        return "Weak - Password must contain at least one uppercase letter"
    if not re.search(r'[0-9]', password):
        return "Weak - Password must contain at least one digit"
    if not re.search(r'[^A-Za-z0-9]', password):
        return "Weak - Password must contain at least one special character"
    
    # If all checks pass, the password is considered strong
    return "Strong"

# Example usage
password = "MyStrongPassword!"
result = assess_password_strength(password)
print(result)
