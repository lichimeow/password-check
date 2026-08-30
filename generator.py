import string
import secrets

def gener(length, lowercase, uppercase, digits, symbols):
    chars=""
    if lowercase:
        chars += string.ascii_lowercase
    if uppercase:
        chars += string.ascii_uppercase
    if digits:
        chars += string.digits
    if symbols:
        chars += string.punctuation
    if not chars:
        return None
    password = ""
    if lowercase:
        password += secrets.choice(string.ascii_lowercase)
    if uppercase:
        password += secrets.choice(string.ascii_uppercase)
    if digits:
        password += secrets.choice(string.digits)
    if symbols:
        password += secrets.choice(string.punctuation)
    for i in range(length - len(password)):
        password += secrets.choice(chars)
    password = list(password)
    secrets.SystemRandom().shuffle(password)
    return "".join(password)