from flask import Flask, render_template, request, redirect, url_for, make_response
import requests
import os
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='דף בית')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         print(request.args)
#         user = request.form.get("username")
#         password = request.form.get("password")
#         print(user, password)
#         return render_template('login.html', title='Login')
#     else:
#         return render_template('login.html', title='Login')


users = {
    "Selector": "SelectorPassOr",
    "EVPlayer": "EV12345",
    "NoVa": "TheGodness1857",
    "RSIL": "RSILPassCode",
}

@app.route('/stafflogin', methods=['GET', 'POST'])
def stafflogin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            error_username = 'חסר שם משתמש'
        else:
            error_username = None

        if not password:
            error_password = 'חסר סיסמה'
        else:
            error_password = None

        if not username or not password:
            return render_template('stafflogin.html', title='Login', error_username=error_username, error_password=error_password)

        # בדיקה אם המשתמש קיים ברשימת המשתמשים והסיסמה תואמת
        if username in users and users[username] == password:
            # אם השם משתמש והסיסמה תואמים, הכניסה מוצלחת
            response = make_response(redirect(url_for('panel')))
            response.set_cookie('username', username)
            return response
        else:
            # אם הכניסה נכשלה, חזור לדף ההתחברות עם הודעת שגיאה
            error_message = 'שם משתמש או סיסמה לא נכונים'
            return render_template('stafflogin.html', title='Login', error_message=error_message)
    else:
        return render_template('stafflogin.html', title='Login')

@app.route('/panel')
def panel():
    username = request.cookies.get('username')
    if username:
        return render_template('panel.html', username=username)
    else:
        return redirect(url_for('stafflogin'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('stafflogin')))
    response.set_cookie('username', '', expires=0)
    return response


    

@app.route('/credits', methods=['GET', 'POST'])
def credits():
    return render_template('credits.html', title='קרדיטים')

@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    return render_template('lesson.html', title='מדריכים')

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    return render_template('ai.html', title='בינה מלאכותית')


@app.route('/updates', methods=['GET', 'POST'])
def updates():
    return render_template('updates.html', title='עדכוני רובלוקס סטודיו')


@app.route('/support', methods=['GET', 'POST'])
def support():
    return render_template('support.html', title='תמיכה')


@app.route('/guides', methods=['GET', 'POST'])
def guides():
    return render_template('guides.html', title='בקשת מדריך')



@app.route('/submit_request', methods=['POST'])
def submit_request():
    message = request.form.get('message')
    issue = request.form.get('issue')
    guide = request.form.get('guide')
    username = request.form.get('username')  # קריאה לשם המשתמש שנשלח כשדה נסתר

    # יצירת הודעת Embed לשליחה לדיסקורד
    discord_embed = {
        "title": "בקשה לעריכת טופס",
        "color": 3447003,
        "fields": [
            {"name": "מה שהוא רצה לערוך ולמה", "value": f"```{message}```", "inline": False},
            {"name": "מה שערכת", "value": f"```{issue}```", "inline": False},
            {"name": "המדריך שהוא רוצה לערוך", "value": f"```{guide}```", "inline": False},
            {"name": "מי שלח את הבקשה", "value": f"```{username}```", "inline": False}
        ]
    }

    # המופע של ה-Webhook שקיבלת מדיסקורד
    webhook_url = "https://discord.com/api/webhooks/1174692269304062042/XFu3GDHUEagyscor9OrBY2_5z8aEMde1thcnYcXkDwenQra2UgYusuJ0wViiap9TPp3W"

    # שליחת הודעה לדיסקורד
    response = requests.post(webhook_url, json={"embeds": [discord_embed]})

    return "הבקשה נשלחה בהצלחה!"


@app.route('/guide_request', methods=['POST'])
def guide_request():
    message = request.form.get('message')
    guide = request.form.get('guide')

    # יצירת הודעת Embed לשליחה לדיסקורד
    discord_embed = {
        "title": "בקשה מדריך",
        "color": 3447003,
        "fields": [
            {"name": "המדריך שהוא רוצה", "value": f"```{message}```", "inline": False},
            {"name": "סוג המדריך שהוא רוצה", "value": f"```{guide}```", "inline": False},
        ]
    }

    # המופע של ה-Webhook שקיבלת מדיסקורד
    webhook_url = "https://discord.com/api/webhooks/1238465521847107584/9VHvaPO7WGurTbQxim0Og7d4qeIOOPilrkEcwsD8D6sVLQlVyk2OSpMxtVmzx3pyYSse"

    # שליחת הודעה לדיסקורד
    response = requests.post(webhook_url, json={"embeds": [discord_embed]})

    return "הבקשה נשלחה בהצלחה!"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ...
