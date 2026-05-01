# app/services/email_service.py
"""
Ampalone Partner Portal - Email Service
Version: 1.0.0
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from app.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email with optional attachments"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = to_email
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach files if provided
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={file_path.split("/")[-1]}'
                        )
                        msg.attach(part)
            
            # Send email
            if settings.DEBUG:
                logger.info(f"Email would be sent to {to_email}: {subject}")
                return True
            
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False


# Global email service instance
email_service = EmailService()


async def send_welcome_email(email: str, company_name: str) -> bool:
    """Send welcome email to new partner"""
    subject = f"Welcome to Ampalone Partner Program - {company_name}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1e40af;">Welcome to Ampalone Partner Program!</h2>
            <p>Dear Partner,</p>
            <p>Thank you for registering with Ampalone Softwares.</p>
            <p><strong>Company Name:</strong> {company_name}</p>
            <p>Our team will review your application within 2-3 business days.</p>
            <h3>Next Steps:</h3>
            <ol>
                <li>Complete your profile in the Partner Portal</li>
                <li>Download and sign the NDA</li>
                <li>Complete product training</li>
                <li>Start tagging customers</li>
            </ol>
            <p style="margin-top: 30px;">
                <a href="https://portal.ampalone.com/login" 
                   style="background-color: #1e40af; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">
                    Access Partner Portal
                </a>
            </p>
            <p style="margin-top: 30px; color: #666; font-size: 14px;">
                Best regards,<br>
                Ampalone Partner Team<br>
                Email: partners@ampalone.com
            </p>
        </div>
    </body>
    </html>
    """
    
    return await email_service.send_email(email, subject, html_content)


async def send_approval_email(email: str, company_name: str) -> bool:
    """Send partner approval email"""
    subject = f"Your Ampalone Partner Application Has Been Approved - {company_name}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #16a34a;">Congratulations! Application Approved</h2>
            <p>Dear Partner,</p>
            <p>Your partner application has been approved.</p>
            <p><strong>Company Name:</strong> {company_name}</p>
            <p><strong>Partner Tier:</strong> Silver</p>
            <p><strong>Margin:</strong> 25%</p>
            <h3>You can now:</h3>
            <ul>
                <li>Tag customers in the Partner Portal</li>
                <li>Generate quotations with up to 60% discount</li>
                <li>Access all product documentation</li>
                <li>Track your pipeline and commissions</li>
            </ul>
            <p style="margin-top: 30px;">
                <a href="https://portal.ampalone.com/login" 
                   style="background-color: #16a34a; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px;">
                    Login to Partner Portal
                </a>
            </p>
        </div>
    </body>
    </html>
    """
    
    return await email_service.send_email(email, subject, html_content)
