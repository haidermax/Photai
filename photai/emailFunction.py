import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'activation@techda.dev'
sender_password = 'KRR%atRz4Vh%'


def send_email(receiver_email, subject, content, sender_email='activation@techda.dev', sender_password='KRR%atRz4Vh%'):
    with smtplib.SMTP_SSL('premium86.web-hosting.com', 465) as smtp:
        smtp.login(sender_email, sender_password)

        # Define the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(MIMEText(content, 'html'))

        # Send the email
        smtp.send_message(message)
    print('Mail Sent!!')


# for i in range(5):
#     send_email('sci4all.info@gmail.com', 'Activate your account', 'This is a test mail to check using python')