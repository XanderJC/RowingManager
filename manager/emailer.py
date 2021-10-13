import smtplib, ssl
from django.conf import settings

port = 465  # For SSL
email_password = settings.EMAIL_HOST_PASSWORD

# Create a secure SSL context
context = ssl.create_default_context()

url = "http://secbc.herokuapp.com"


def sendSignupDetails(crsid, password):
    sent_from = 'secbc.web@gmail.com'
    send_to = crsid + "@cam.ac.uk"
    subject = 'Welcome to St. Edmunds College Boat Club'

    headers = [
        "From: " + sent_from,
        "Subject: " + subject,
        "To: " + send_to,
        "MIME-Version: 1.0",
        "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    body = """<html>
      <head></head>
      <body>
      <p>Welcome to the SECBC website! Sign in at http://secbc.herokuapp.com using """+password+""" as your password.</p>
      <p>Please remember to change your password after you've logged in</p>
      <p>HOW TO SIGN UP FOR ERG SESSIONS: Go to login -> Sign up for outings as a rower -> Click 'join' on any erg times for which you may be available</p>
      <p>Once you've marked yourself as available, the captains may assign you a spot on any of your available days.</p>
      <p>TO SEE IF YOU'VE BEEN ALLOTED FOR AN ERG SESSION: Check 'view my outings' a bit later (We'll also be sending out mails).</p>
      </body></html>
      """

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sent_from, email_password)
        server.sendmail(sent_from, send_to, headers + "\r\n\r\n" + body)