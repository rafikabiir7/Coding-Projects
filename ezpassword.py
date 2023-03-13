import re
import math

def check_password_strength(password):
    if len(password) < 8:
        return "weak"
    elif len(password) >= 8 and len(password) < 12:
        return "medium"
    else:
        return "strong"

def calculate_crack_time(password):
    upper = r'[A-Z]'
    lower = r'[a-z]'
    digit = r'\d'
    special = r'[!@#$%^&*()_+=\-{}\[\]:;<>,.?\/]'
    patterns = [upper, lower, digit, special]
    score = 0
    for pattern in patterns:
        if re.search(pattern, password):
            score += 1
    entropy = math.log((score ** len(password)), 2)
    seconds_to_crack = 2 ** entropy / 2
    days_to_crack = seconds_to_crack / (60 * 60 * 24)
    return min(int(days_to_crack), 10000)

password = input("Enter a password: ")
strength = check_password_strength(password)
days_to_crack = calculate_crack_time(password)

if days_to_crack > 10000:
    days_to_crack = "more than 10,000"
else:
    days_to_crack = str(days_to_crack)

print("Your password is", strength, "and it would take", days_to_crack, "days to crack.")

