import argparse
import datetime
import json
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_CONFIG = {
    'sender': 'FEUP - Faturas',
    'subject': 'Nova fatura disponível',
    'server': 'smtp.gmail.com',
    'port': 587,
    'username': 'feupsr@gmail.com',
    'password': 'ouxwkrviwcjnahfd'
}

# Load a file and return its contents
def load_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

# Load the email body from the email.html file
def load_email_body():
    return load_file('emailBody.html')
    
# Load the html file to send as attachment
def load_attach_file():
    return load_file('attach_encoded.html')

# Load the emails from the emails.json file into an array
def load_email_array():
    with open('emails.json', 'r') as f:
        return json.load(f).get('emails')
    

# Send an email with an attachment
def send_email(email, html_attachment_body, html_attachment_filename, html_email_body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = email
    msg['Subject'] = EMAIL_CONFIG['subject']

    # Add the html to the email
    msg.attach(MIMEText(html_email_body, 'html'))

    # Create the attachment
    part = MIMEApplication(html_attachment_body)
    part.add_header('Content-Disposition',
                    'attachment', filename=html_attachment_filename)
    msg.attach(part)

    # Send the email
    server = smtplib.SMTP(EMAIL_CONFIG['server'], EMAIL_CONFIG['port'])
    server.starttls()
    server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
    print(f'Sending email to {email}')
    server.sendmail(EMAIL_CONFIG['sender'], email, msg.as_string())
    server.quit()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send emails with attachments.')
    parser.add_argument('backend_route', help='The backend route.')
    args = parser.parse_args()

    # Load email body, attach file, email array
    html_email_body = load_email_body()
    emails = load_email_array()
    html_attachment_body = load_attach_file()

    # Change ${backendRoute} to the backend route
    html_attachment_body = html_attachment_body.replace('${backendRoute}', args.backend_route)

    # Send the email to each email in the emails array
    for email in emails:
        # Change ${userEmail} to the email address of the current user
        html_attachment_body_replaced = html_attachment_body.replace('${userEmail}', email)

        # Get current date
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Create a string with 'Fatura_${currentDate}.html'
        html_attachment_filename = f'Fatura_{current_date}.html'

        # Send the email
        send_email(email, html_attachment_body_replaced, html_attachment_filename, html_email_body)


if __name__ == '__main__':
    main()
