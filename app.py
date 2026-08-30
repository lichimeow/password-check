from flask import Flask, render_template, request
from checker import pass_score
from generator import gener
app = Flask(__name__)
@app.route("/", methods=["GET","POST"])
def index():
    check_error = None
    generator_error = None
    score=None
    advice=[]
    generated = None    
    password = ""
    status = None
    if request.method =="POST":
        if "check" in request.form:
            password = request.form.get("password", "")
            if password == "":
                check_error = "Введите пароль для проверки."
            else:
                score, advice = pass_score(password)
                if score is not None:
                    if score<40:
                        status = "Слабый пароль"
                    elif score < 70:
                        status  = "Средний пароль"
                    else:
                        status = "Надёжный пароль"
                else:
                    status = None
        elif "generate" in request.form:
            length = int(request.form.get("length",16))
            lowercase = "lowercase" in request.form
            uppercase = "uppercase" in request.form
            digits = "digits" in request.form
            symbols = "symbols" in request.form

            categories = sum([
                lowercase,
                uppercase,
                digits,
                symbols
            ])

            if categories == 0:
                generator_error = "Выберите хотя бы один тип символов."
            elif length < categories:
                generator_error = f"Для выбранных типов символов нужна длина минимум {categories}"
            else:
                generated = gener(
                    length,
                    lowercase,
                    uppercase,
                    digits,
                    symbols
                )
    return render_template (
        "index.html",
        score=score,
        status=status,
        advice=advice,
        password=password,
        generated=generated,
        check_error=check_error,
        generator_error=generator_error
        )
if __name__ == "__main__":
    app.run(debug=True)