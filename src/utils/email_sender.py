import yagmail
from dotenv import load_dotenv
load_dotenv()
import os
def queue_email(recipient: str, pdf_path: str) -> bool:
    try:
        sender_email = os.getenv("FITAGENT_EMAIL")
        sender_pass = os.getenv("FITAGENT_EMAIL_PASS")
        if not sender_email or not sender_pass:
            raise ValueError("Missing email credentials in environment variables")

        yag = yagmail.SMTP(user=sender_email, password=sender_pass)
        subject = "Your Personalized Meal Plan from FitAgent"
        body = "Hello!\n\nAttached is your personalized meal and fitness plan.\nStay healthy and consistent!\n\n– FitAgent AI"

        yag.send(to=recipient, subject=subject, contents=body, attachments=pdf_path)
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False