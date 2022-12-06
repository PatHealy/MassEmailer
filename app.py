from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

#################################
# Helper functions
#################################

def get_people(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    people = pd.read_csv(url)
    names = [name.split()[0] for name in people.Name]
    emails = [email for email in people.Email]
    return [(names[i], emails[i]) for i in range(len(names))], emails

#################################
# Routes
#################################

@app.route('/')
def hello_world():
    return render_template('setup.html')

@app.route('/message', methods=['POST', 'GET'])
def message_sender():
    sheet_link = request.form["sheet_link"]
    sheet_link = sheet_link[sheet_link.index("/d/") + 3:]
    sheet_id = sheet_link[:sheet_link.index("/")]
    sheet_name = request.form["sheet_name"]
    people, emails = get_people(sheet_id, sheet_name)
    subject = request.form["subject"]
    email_body = request.form["email_body"]
    return render_template(
        "sender.html",
        people=people,
        subject=subject,
        email_body="\n%0d%0a\n%0d%0a" + email_body.replace("\n", "\n%0d%0a"),
        emails=str(emails)
    )