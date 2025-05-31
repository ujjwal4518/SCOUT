import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import traceback


def send_alert(sender_email, sender_password, recipient_email):
    """
    Sends an email alert without a video attachment.
    
    Args:
        sender_email (str): Email address of the sender.
        sender_password (str): Password or app-specific password for the sender's email.
        recipient_email (str): Email address of the recipient.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Fire Alert"
        body = (
            "Dear User,\n\n"
            "An fire was detected by our monitoring system. "
            "Please check the live feed or logs for more details.\n\n"
            "Best regards,\nYour Security System"
        )
        
        # Attach email body
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using SMTP
        print("Connecting to SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email alert sent successfully!")
    
    except Exception as e:
        print(f"Error sending email alert: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Example usage
    sender_email = "shyam451807@gmail.com"
    sender_password = "zuie mfpm zeku jaxp"  # Use App Password if Gmail
    recipient_email = "ujjwaldwivedi567@gmail.com"
    
    # Send alert
    send_alert(sender_email, sender_password, recipient_email)
