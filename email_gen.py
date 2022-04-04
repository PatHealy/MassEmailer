from datetime import date
import pandas as pd

#Read in email text
lines = []
with open("email_text.txt") as rf:
	lines = rf.readlines()

#Subject line is the first line
subject = lines[0].strip()

#Parse Text
vspace = " %0d%0a"
email_txt = vspace[1:] + vspace + "\n"
lines = lines[1:]
for line in lines:
	if len(line) > 1:
		email_txt = email_txt + line.strip() + vspace + "\n"
	else:
		email_txt = email_txt + vspace[1:] + "\n"

#Read in people and contact info. Only uses first name
people = pd.read_excel("to_send.xlsx")
names = [name.split()[0] for name in people.Name]
emails = [email for email in people.Email]

#Create HTML file full of email links with embedded info
body = """<html><head></head><body>"""
for i in range(len(names)):
	nm = names[i]
	email = emails[i]
	ln = """<a id=\"""" + email + """\" href=\"""" + "mailto:" + email + "?subject=" + subject + "&body=" + nm + ", " + email_txt + """\">Send email to """ + nm + ", " + email + """</a><br/><br/>"""
	body = body + ln

body = body + """
	<script>
		function mark_clicked(evt){
			em = evt.currentTarget.id;
			console.log(em);
			var el = document.getElementById(em);
			var txt = document.createTextNode(\" Emailed!\");
			el.appendChild(txt);
		}
		var emails = """ + str(emails) + """;
		var i = 0;
		for(i = 0; i < emails.length; i++){
			document.getElementById(emails[i]).addEventListener(\"click\", mark_clicked);
		}
	</script>
	</body></html>
"""

#Save file
today = date.today()
with open("email_automater_" + subject + "_" + today.strftime("%d-%m-%Y") + ".html", "w+") as wf:
	wf.write(body)

print('done')
