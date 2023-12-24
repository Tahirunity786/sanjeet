import base64
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)


def email_sender(email, pdf_filename, media):
    try:
        message = Mail(
            from_email="info@backupdoc.ai",
            to_emails=email,
            subject="Your AI-Generated Dental Report from BackupDoc.ai",
            html_content=(
                """
                <html>
                <body style="font-family: Arial; font-size: 14px;">
                    <h1 style="font-family: Arial; font-size: 20px;">Backupdoc</h1>
                    <p>
                        We hope you're doing well. As part of our commitment to providing you with innovative dental health solutions, we have completed an AI-generated analysis of your recent dental radiographs using <a href="https://www.backupdoc.ai" target="_blank">BackupDoc</a>. This report offers a preliminary overview of your dental health based on the latest AI technology.
                    </p>
                    <p>
                        Attached to this email, you will find:
                        <ul>
                            <li>AI-Generated Dental Report</li>
                        </ul>
                    </p>
                    <p>
                        Understanding Your Report: Your report provides an initial analysis of your dental radiographs, highlighting areas that may require attention. It's designed to give you insights that can facilitate more informed discussions with your dentist.
                    </p>
                    <p>
                        Recommendations: While this report offers valuable information, it's crucial to follow up with a dental professional for a comprehensive evaluation and diagnosis.
                    </p>
                    <p>
                        Next Steps: Please review the attached report and consider scheduling an appointment with your dentist for further assessment and personalized advice.
                    </p>
                    <p>
                        Disclaimer: Please be aware that this AI-generated report is intended for informational purposes only and does not constitute medical advice, diagnosis, or treatment. <a href="https://www.backupdoc.ai" target="_blank">BackupDoc</a> provides a preliminary analysis which should not replace professional dental evaluations. The accuracy of the report is based on the quality of the radiograph provided and current AI capabilities. Always consult with a qualified dentist for any dental concerns or before making any decisions based on this report. <a href="https://www.backupdoc.ai" target="_blank">BackupDoc</a> is not liable for any actions taken based on this report without professional dental advice.
                    </p>
                    <p>
                        Thank you for using <a href="https://www.backupdoc.ai" target="_blank">BackupDoc</a> for your preliminary dental analysis. We are dedicated to empowering you with the latest tools for better dental health.
                    </p>
                    <p>
                        Best regards,
                    </p>
                    <p>
                        The <a href="https://www.backupdoc.ai" target="_blank">BackupDoc</a> Team
                    </p>
                </body>
                </html>
                """
            ),
        )
        
        media_path = media
        with open(media_path, "rb") as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("image/jpeg")
        attachment.file_name = FileName("Analyzed image.jpeg")
        attachment.disposition = Disposition("attachment")
        message.attachment = attachment
    

        with open(pdf_filename, "rb") as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("application/pdf")
        attachment.file_name = FileName("Report.pdf")
        attachment.disposition = Disposition("attachment")
        message.attachment = attachment
        try:
            sg = SendGridAPIClient(
                "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"
            )
            response = sg.send(message)
            return response
        except:
            return "Not sent"

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  # re-raise the exception to see its traceback
