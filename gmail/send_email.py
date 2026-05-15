import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def build_mime_message(sender, to, subject, body_text):
    msg = MIMEMultipart()

    msg['To'] = to
    msg['From'] = sender
    msg['Subject'] = subject

    msg.attach(MIMEText(body_text, 'plain'))

    raw = base64.urlsafe_b64encode(
        msg.as_bytes()
    ).decode()

    return {'raw': raw}


def send_email(service, sender, to, subject, body_text):

    message = build_mime_message(
        sender,
        to,
        subject,
        body_text
    )

    sent_message = service.users().messages().send(
        userId='me',
        body=message
    ).execute()

    return sent_message