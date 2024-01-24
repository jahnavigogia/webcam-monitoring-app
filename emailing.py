import imghdr
import smtplib
import ssl
import imghdr
from email.message import EmailMessage

username = "send.email.sendd@gmail.com"
password = "butaxyhwrkhtlyzm"
receiver = "jahnavigogia20@gmail.com"


def send_email(img_path):
    print("send email function started.")
    email_msg = EmailMessage()
    email_msg['Subject'] = "New customer showed up!"
    email_msg.set_content("Hey, we just saw a new customer")
    with open(img_path, "rb") as file:
        content = file.read()
        email_msg.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)

    gmail.sendmail(username, receiver, email_msg.as_string())
    gmail.quit()
    print("Clean folder function exited.")


if __name__ == "__main__":
    send_email(img_path="images/55.png")
