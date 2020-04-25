def contains_one_letter(password):
    for letter in password:
        if letter.isalpha():
            return True
    return False

def contains_one_digit(password):
    for letter in password:
        if letter.isdigit():
            return True
    return False

def contains_repeating_characters(password):
    for i in range(0, len(password)-2):
        if password[i] == password[i+1] == password[i+2]:
            return True
    return False

def strong_password(password):

    if len(password) < 8 or len(password) > 15:
        return "Invalid Password"

    letter = contains_one_letter(password)
    digit = contains_one_digit(password)
    repeating = contains_repeating_characters(password)

    if letter == True and digit == True and repeating == False:
        return "Strong Password"
    else:
        return "Weak Password"

print(strong_password("123abc"))
print(strong_password("123456789abcdefg"))
print(strong_password("12345AbcD"))
print(strong_password("11213abcd"))
print(strong_password("11145abcd"))
print(strong_password("12aaaaabcd"))
print(strong_password("1234567890"))
print(strong_password("abCdefGhiJ"))
print("-----")
print(strong_password("1234567bbb"))
print(strong_password("1234567bb"))








