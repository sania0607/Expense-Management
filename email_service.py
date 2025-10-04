"""
Email Service for Expense Management System
Handles sending emails for password resets and notifications
"""

import smtplib
import ssl
import os
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'admin@company.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.sender_name = os.getenv('SENDER_NAME', 'Expense Management System')
        
    def generate_random_password(self, length=12):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def send_password_reset_email(self, user_email, user_name, new_password):
        """Send password reset email to user"""
        
        # Check if email is properly configured
        if not self.sender_password or self.sender_password == 'your-app-password':
            print(f"⚠️ Email not configured. Password for {user_name}: {new_password}")
            return False, f"Email not configured. Password is: {new_password}"
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset - Expense Management System"
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = user_email
            
            # Create the HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                             color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .password-box {{ background: #fff; border: 2px solid #667eea; padding: 15px; 
                                   margin: 20px 0; text-align: center; border-radius: 8px; }}
                    .password {{ font-family: 'Courier New', monospace; font-size: 18px; 
                               font-weight: bold; color: #667eea; letter-spacing: 2px; }}
                    .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; 
                             font-size: 12px; color: #666; }}
                    .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; 
                              border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Password Reset</h1>
                        <p>Expense Management System</p>
                    </div>
                    <div class="content">
                        <h2>Hello {user_name},</h2>
                        <p>Your password has been reset by a system administrator. Below is your new temporary password:</p>
                        
                        <div class="password-box">
                            <p><strong>Your New Password:</strong></p>
                            <div class="password">{new_password}</div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important Security Notice:</strong>
                            <ul>
                                <li>Please change this password immediately after logging in</li>
                                <li>Do not share this password with anyone</li>
                                <li>Use a strong, unique password for your account</li>
                            </ul>
                        </div>
                        
                        <p><strong>How to log in:</strong></p>
                        <ol>
                            <li>Go to the expense management system login page</li>
                            <li>Use your email address: <strong>{user_email}</strong></li>
                            <li>Use the temporary password provided above</li>
                            <li>Change your password in your profile settings</li>
                        </ol>
                        
                        <p>If you did not request this password reset or have any concerns, please contact your system administrator immediately.</p>
                        
                        <div class="footer">
                            <p>This email was sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                            <p>© 2025 Expense Management System. This is an automated message, please do not reply.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Create plain text version
            text_content = f"""
            Password Reset - Expense Management System
            
            Hello {user_name},
            
            Your password has been reset by a system administrator.
            
            Your new temporary password is: {new_password}
            
            IMPORTANT SECURITY NOTICE:
            - Please change this password immediately after logging in
            - Do not share this password with anyone
            - Use a strong, unique password for your account
            
            How to log in:
            1. Go to the expense management system login page
            2. Use your email address: {user_email}
            3. Use the temporary password provided above
            4. Change your password in your profile settings
            
            If you did not request this password reset, please contact your system administrator.
            
            This email was sent on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            """
            
            # Attach parts
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            message.attach(part1)
            message.attach(part2)
            
            # Send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
                
                text = message.as_string()
                server.sendmail(self.sender_email, user_email, text)
            
            return True, "Email sent successfully"
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            # More detailed error info
            if "535" in str(e):
                print("🔍 Gmail Error 535: Authentication failed")
                print("✅ Solutions:")
                print("   1. Enable 2-Step Verification in Gmail")
                print("   2. Generate App Password (not regular password)")
                print("   3. Use 16-character app password in .env file")
            return False, f"Failed to send email: {str(e)}"
    
    def test_email_connection(self):
        """Test email server connection"""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                if self.sender_password:
                    server.login(self.sender_email, self.sender_password)
            return True, "Email connection successful"
        except Exception as e:
            return False, f"Email connection failed: {str(e)}"

# Initialize global email service
email_service = EmailService()