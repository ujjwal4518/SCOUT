import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import traceback


def send_intruder_alert(sender_email, sender_password, recipient_email, video_path):
    """
    Sends an email alert with a video attachment when an intruder is detected.
    
    Args:
        sender_email (str): Email address of the sender.
        sender_password (str): Password or app-specific password for the sender's email.
        recipient_email (str): Email address of the recipient.
        video_path (str): Path to the intruder video file to attach.
    """
    try:
        # Validate video file exists
        if not os.path.exists(video_path):
            print(f"Error: The video file '{video_path}' does not exist.")
            return
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "🚨 Intruder Detected Alert - Video Recording"
        body = (
            "Dear User,\n\n"
            "An intruder was detected by your monitoring system. "
            "Please find the attached video recording for review.\n\n"
            "Stay safe,\nYour Security System"
        )
        
        # Attach email body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach video file
        with open(video_path, "rb") as file:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(file.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(video_path)}'
            )
            msg.attach(mime_base)
        
        # Send email using SMTP
        print("Connecting to SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Intruder alert sent successfully!")
    
    except Exception as e:
        print(f"Error sending intruder alert: {e}")
        print(traceback.format_exc())


if __name__ == "_main_":
    # Example usage
    sender_email = "shyam451807@gmail.com"
    sender_password = "zuie mfpm zeku jaxp"  # Use App Password if Gmail
    recipient_email = "ujjwaldwivedi567@gmail.com"
    video_path = "recording_intruder.avi"  # Replace with the actual video file path
    
    # Send intruder alert
    send_intruder_alert(sender_email, sender_password, recipient_email, video_path)