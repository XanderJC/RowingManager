import smtplib, ssl
from django.conf import settings

from manager.models import InOuting, HasBeenMailedOuting, Outing

port = 465  # For SSL
email_password = settings.EMAIL_HOST_PASSWORD

# Create a secure SSL context
context = ssl.create_default_context()

url = "http://wcbc-manager.herokuapp.com"


def sendOutingReminders(outing_id):
    outing = Outing.objects.get(id=outing_id)
    crsids = []

    body = (
        """<html>
              <head></head>
              <body>
              <p>Dear rower/cox/coach,</p>
              <p>You have an outing coming up on """
        + str(outing.date)
        + " at "
        + str(outing.meetingTime)
        + """.</p>
              <p>You can check your upcoming outings at http://wcbc-manager.herokuapp.com/myOutings/</p>
              <p>/WCBC Website</p>
              </body></html>
              """
    )

    # Todo can be made more robust
    for inOuting in InOuting.objects.filter(outing=outing):
        person = inOuting.person

        if (
            HasBeenMailedOuting.objects.filter(person=person, outing=outing).count()
            == 0
        ):
            crsids += [person.username]
            HasBeenMailedOuting(person=person, outing=outing).save()

    send_email(crsids, "[WCBC WEBSITE] Outing Reminder", body)


# Todo Use Django email api instead
def send_email(crsids, subject, body):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sent_from = "wolfson.captain@cucbc.org"
        server.login(sent_from, email_password)
        i = True
        for email in [crsid + "@cam.ac.uk" for crsid in crsids]:
            send_to = email
            headers = [
                "From: " + sent_from,
                "Subject: " + subject,
                "To: " + email,
                "MIME-Version: 1.0",
                "Content-Type: text/html",
            ]
            if i:
                headers += ["CC: wolfson.captain@cucbc.org"]
                i = False
            headers = "\r\n".join(headers)
            server.sendmail(sent_from, send_to, headers + "\r\n\r\n" + body)


def sendSignupDetails(crsid, password):
    sent_from = "wolfson.captain@cucbc.org"
    send_to = crsid + "@cam.ac.uk"
    subject = "Welcome to Wolfson College Boat Club"

    headers = [
        "From: " + sent_from,
        "Subject: " + subject,
        "To: " + send_to,
        "MIME-Version: 1.0",
        "Content-Type: text/html",
    ]
    headers = "\r\n".join(headers)

    body = (
        """<html>
      <head></head>
      <body>
      <p>Welcome to the WCBC website! Sign in at http://wcbc-manager.herokuapp.com using """
        + password
        + """ as your password.</p>
      <p>Please remember to change your password after you've logged in</p>
      </body></html>
      """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sent_from, email_password)
        server.sendmail(sent_from, send_to, headers + "\r\n\r\n" + body)
