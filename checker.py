import math
import string
import os
ADVICE = {
    "short": "Увеличьте длину пароля (минимум 12 символов)",
    "low_entropy": "Используйте больше разных типов символов",
    "rep": "Уберите повторяющиеся последовательности символов",
    "common": "Этот пароль слишком распространен. Придумайте уникальный пароль",
    "dig": "Добавьте цифры в пароль",
    "sym": "Добавьте специальные символы",
    "low": "Добавьте строчные буквы",
    "up": "Добавьте заглавные буквы"
}
def calc_alp(password):
    alp = 0
    if any(c.islower() for c in password):
        alp +=26
    if any(c.isupper() for c in password):
        alp+=26
    if any(c.isdigit() for c in password):
        alp+=10
    if any(c in string.punctuation for c in password):
        alp += len(string.punctuation)
    return alp

def symb(password):
    advice=[]
    points = 0
    if any(c.isdigit() for c in password):
        points += 5
    else:
        advice.append(ADVICE["dig"])

    if any(c in string.punctuation for c in password):
        points += 5
    else:
        advice.append(ADVICE["sym"])

    if any(c.islower() for c in password):
        points += 5
    else:
        advice.append(ADVICE["low"])

    if any(c.isupper() for c in password):
        points += 5
    else:
        advice.append(ADVICE["up"])
    return points, advice

def calc_entropy(password):
    advice = []
    alp = calc_alp(password)
    if alp==0:
        return 0, [ADVICE["low_entropy"]]
    entropy = len(password) * math.log2(alp)
    if entropy < 30:
        advice.append(ADVICE["low_entropy"])
        return 0, advice
    elif entropy < 50:
        return 10, advice
    elif entropy < 70:
        return 20, advice
    else:
        return 30, advice

def repeat(password, length=3):
    advice =[]
    for i in range(len(password)-length+1):
        part = password[i:i+length]
        if part in password[i+length:]:
            advice.append(ADVICE["rep"])
            return 0, advice
    return 20, advice

def check_leng(password):
    advice = []
    leng = len(password)
    if leng < 8:
        advice.append(ADVICE["short"])
        return 0, advice
    elif leng <12:
        advice.append(ADVICE["short"])
        return 10, advice
    elif leng < 16:
        return 20, advice
    else:
        return 30, advice

def common_pass(password):
    path = os.path.join(
        os.path.dirname(__file__),
        "common_passwords.txt"
    )
    with open(path,"r") as file:
        passwords = file.read().splitlines()
    if password.lower() in passwords:
        return True
    return False

def pass_score(password):
    advice= []
    score = 0
    if common_pass(password):
        return 0, [ADVICE["common"]]
    
    points,tips = calc_entropy(password)
    score += points
    advice.extend(tips)

    points, tips= check_leng(password)
    score += points
    advice.extend(tips)

    points, tips = symb(password)
    score += points
    advice.extend(tips)

    points, tips = repeat(password)
    score += points
    advice.extend(tips)


    if score > 100:
        score = 100
        
    return score, advice
    
