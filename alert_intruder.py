import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import traceback

def send_alert(sender_email, sender_password, recipient_email, video_path):
    """
    Sends an email alert with a video attachment.
    
    Args:
        sender_email (str): Email address of the sender.
        sender_password (str): Password or app-specific password for the sender's email.
        recipient_email (str): Email address of the recipient.
        video_path (str): Path to the video file to attach.
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
        msg['Subject'] = "Intruder-Detected - Video Recording"
        body = (
            "Dear User,\n\n"
            "A intruder was detected by our monitoring system. "
            "The recording has been started and saved.\n\n"
            "Best regards,\nYour Security System"
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
            print("Email alert sent successfully!")
    
    except Exception as e:
        print(f"Error sending email alert: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Example usage
    sender_email = "shyam451807@gmail.com"
    sender_password = "zuie mfpm zeku jaxp"  # Use App Password if Gmail
    recipient_email = "ujjwaldwivedi567@gmail.com"
    video_path = "recording_20250416_152047.avi"  # Replace with your video file path
    
    # Send alert
    send_alert(sender_email, sender_password, recipient_email, video_path)
