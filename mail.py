import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dotenv
import os

dotenv.load_dotenv()

class Mail:
    def __init__(self, from_email: str,
                  to_email: str,
                  host: str = "smtp.gmail.com", 
                  port: int = 587):
        self.from_email = from_email
        self.to_email = to_email
        self.host = host
        self.port = port
        self.app_password = os.getenv("mail_sender_password")

    def send_email(self, title: str,
                    message: str = "OTP email verification",
                    attachment = None):
        msg = EmailMessage()
        msg['Subject'] = title
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg.set_content(message)
        try:
            if attachment:
                extension = attachment[attachment.rfind(".")+1:] 
                match extension:
                    case "png":
                        main_type = "image"
                    case "jpeg":
                        main_type = "image"
                    case "pdf":
                        main_type = "pdf"
                    case _:
                        main_type = "image"
                with open(attachment, "rb") as attachment_file:
                    msg.add_attachment(
                        attachment_file.read(),
                        maintype=main_type,
                        subtype=extension,
                        filename=attachment[:attachment.rfind(".")]
                    )
            
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.from_email, self.app_password)
                server.send_message(msg)
                print("Mail was sent succsessfully")
        except Exception as e:
            print(f"Something went wrong: {e}")
    
    def send_html_email(self, title: str, html_data: str = ""):
        new_mail = MIMEMultipart("alternative")
        new_mail['Subject'] = title
        new_mail['From'] = self.from_email
        new_mail['To'] = self.to_email

        if not html_data:
            with open("./templates/email_otp.html", "r") as f:
                html_data = f.read()
        mime_mail = MIMEText(html_data, "html")
        new_mail.attach(mime_mail)

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.from_email, self.app_password)
            server.send_message(new_mail)
            print("Email sent successfully")

if __name__ == '__main__':
    from_email = os.getenv("from_email")
    new_mail = Mail(from_email, from_email)
    new_mail.send_html_email("Please verify your email.")



