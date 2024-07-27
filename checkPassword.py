import re
import math

# List of common passwords to avoid
common_passwords = [
    '123456', 'password', '123456789', '12345678', '12345', '1234567',
    '1234567890', 'qwerty', 'abc123', '111111', 'letmein', '123123'
]

# Example dictionary words list (for simplicity, it's short; extend as needed)
dictionary_words = ['password', 'letmein', 'admin', 'welcome', 'login']

def check_common_passwords(password):
    """
    Check if the password is among common, weak passwords.
    """
    return password.lower() in common_passwords

def check_dictionary_words(password):
    """
    Check if the password contains any dictionary words.
    """
    password_lower = password.lower()
    return any(word in password_lower for word in dictionary_words)

def check_sequences_repetitions(password):
    """
    Check for sequences or repeated characters in the password.
    """
    sequential = bool(re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()))
    repeated = bool(re.search(r'(.)\1{2,}', password))
    return sequential, repeated

def password_criteria(password):
    """
    Check the password against various criteria: length, uppercase, lowercase,
    numbers, and special characters.
    """
    length = len(password) >= 8
    upper = bool(re.search(r'[A-Z]', password))
    lower = bool(re.search(r'[a-z]', password))
    number = bool(re.search(r'[0-9]', password))
    special = bool(re.search(r'[\W_]', password))
    
    return length, upper, lower, number, special

def calculate_entropy(password):
    """
    Estimate the entropy of the password, which is a measure of its randomness.
    """
    char_set = 0
    if re.search(r'[a-z]', password):
        char_set += 26
    if re.search(r'[A-Z]', password):
        char_set += 26
    if re.search(r'[0-9]', password):
        char_set += 10
    if re.search(r'[\W_]', password):
        char_set += 32 # Rough estimate for special characters
    
    # Entropy calculation: log2(char_set) * length
    entropy = len(password) * math.log2(char_set) if char_set else 0
    return entropy

def give_feedback(criteria, dictionary_found, sequences_repetitions):
    """
    Provide feedback to improve the password strength based on unmet criteria.
    """
    length, upper, lower, number, special = criteria
    sequential, repeated = sequences_repetitions
    feedback = []
    
    if not length:
        feedback.append("The password should be at least 8 characters long.")
    if not upper:
        feedback.append("Add uppercase letters to increase strength.")
    if not lower:
        feedback.append("Add lowercase letters to increase strength.")
    if not number:
        feedback.append("Add numbers to increase strength.")
    if not special:
        feedback.append("Add special characters (e.g., @, #, !) to increase strength.")
    if dictionary_found:
        feedback.append("Avoid using common dictionary words in your password.")
    if sequential:
        feedback.append("Avoid using sequences of characters (like 'abc' or '123').")
    if repeated:
        feedback.append("Avoid repeated characters (like '111' or 'aaa').")
    
    return feedback

def password_strength(password):
    """
    Determine the strength of the password and provide feedback.
    """
    if check_common_passwords(password):
        return "Your password is too common and easily guessable. Choose a more secure password."

    dictionary_found = check_dictionary_words(password)
    sequences_repetitions = check_sequences_repetitions(password)
    criteria = password_criteria(password)
    entropy = calculate_entropy(password)

    score = sum(criteria) - int(dictionary_found or any(sequences_repetitions))
    
    if score >= 5:
        return f"Very Strong (Entropy: {entropy:.2f})"
    elif score >= 4:
        return f"Strong (Entropy: {entropy:.2f})"
    elif score >= 3:
        return f"Medium (Entropy: {entropy:.2f})"
    elif score >= 2:
        return f"Weak (Entropy: {entropy:.2f})"
    else:
        return f"Very Weak (Entropy: {entropy:.2f})"

# Main execution
password = input("Enter your password: ")
strength = password_strength(password)

print(f"Your password is: {strength}")

# Provide feedback if the password is not very strong
if "Very Strong" not in strength:
    dictionary_found = check_dictionary_words(password)
    sequences_repetitions = check_sequences_repetitions(password)
    criteria = password_criteria(password)
    feedback = give_feedback(criteria, dictionary_found, sequences_repetitions)
    for tip in feedback:
        print(tip)




