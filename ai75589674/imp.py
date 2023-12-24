# def generate_pdf(request):
#     try:
#         if request.method == "POST":
#             # Token Validation
#             token = request.POST.get("token")

#             try:
#                 if Black_token.objects.filter(token1=token).exists():
#                     grr = request.POST.get("g-recaptcha-response")
#                     sscptcha = settings.captcha_site_key
#                     clinic_name = "BackupDoc"

#                     captchadata = {"secret": sscptcha, "response": grr}
#                     secret_r = requests.post(
#                         "https://www.google.com/recaptcha/api/siteverify",
#                         data=captchadata,
#                     )
#                     response = json.loads(secret_r.text)
#                     verify = response["success"]
#                     if verify:
#                         try:
#                             user_report = UserReport.objects.get(
#                                 user_token__token1=token
#                             )

#                             # Create a BytesIO buffer to receive the PDF data.
#                             buffer = io.BytesIO()

#                             # Create the PDF object, using the BytesIO buffer as its "file."
#                             doc = SimpleDocTemplate(buffer, pagesize=letter)

#                             # Clinic name, user email, and report text
#                             clinic_name = user_report.clinic_name
#                             user_email = user_report.email
#                             report_text = user_report.report

#                             # Create a list to hold the flowables, which will be added to the PDF.
#                             elements = []

#                             # Clinic name (top left)
#                             clinic_name_style = ParagraphStyle(
#                                 name="ClinicName", fontSize=16, alignment=0
#                             )
#                             clinic_name_text = Paragraph(clinic_name, clinic_name_style)
#                             elements.append(clinic_name_text)

#                             # Current datetime (top right)
#                             current_datetime = user_report.date.strftime("%Y-%m-%d %H:%M:%S")
#                             current_datetime_style = ParagraphStyle(
#                                 name="CurrentDatetime", fontSize=10, alignment=2
#                             )
#                             current_datetime_text = Paragraph(current_datetime, current_datetime_style)
#                             elements.append(current_datetime_text)

#                             # Horizontal line
#                             elements.append(Spacer(1, 12))

#                             # User email
#                             user_email_style = ParagraphStyle(
#                                 name="UserEmail", fontSize=12
#                             )
#                             user_email_text = Paragraph(
#                                 f"User Email: {user_email}", user_email_style
#                             )
#                             elements.append(user_email_text)

#                             # Report text
#                             report_text_style = getSampleStyleSheet()["Normal"]
#                             report_text = Paragraph(report_text, report_text_style)
#                             elements.append(report_text)

#                             # Add some space
#                             elements.append(Spacer(1, 12))

#                             # Thank you message
#                             thank_you_style = ParagraphStyle(
#                                 name="ThankYou", fontSize=14, textColor=colors.green
#                             )
#                             thank_you_text = Paragraph("Thank you!", thank_you_style)
#                             elements.append(thank_you_text)

#                             # Build the PDF document and close the buffer.
#                             doc.build(elements)
#                             buffer.seek(0)

#                             # Save the PDF to the media/reports folder
#                             file_name = "dynamic_pdf.pdf"
#                             file_path = os.path.join(
#                                 settings.MEDIA_ROOT, "reports", file_name
#                             )
#                             with open(file_path, "wb") as pdf_file:
#                                 pdf_file.write(buffer.read())

#                             # Create a URL for the saved PDF
#                             pdf_url = os.path.join(
#                                 settings.MEDIA_URL, "reports", file_name
#                             )

#                             return HttpResponse(pdf_url)
#                         except Exception as e:
#                             return HttpResponse(f"Problem :: {e}")
#                     else:
#                         return HttpResponse("Please verify that you are not a robot!")
#                 else:
#                     return HttpResponse("Please! Upload your image")
#             except Exception as e:
#                 return HttpResponse(f"Problem :: {e}")
#         else:
#             return HttpResponse("Bad request")
#     except Exception as e:
#         return HttpResponse(f"Problem :: {e}")
    
    
# def generate_pdf(request):
#     if request.method != "POST":
#         return HttpResponse("Bad request")

#     token = request.POST.get("token")
#     if not Black_token.objects.filter(token1=token).exists():
#         return HttpResponse("Please upload your image")

#     grr = request.POST.get("g-recaptcha-response")
#     sscptcha = settings.captcha_site_key

#     captchadata = {"secret": sscptcha, "response": grr}
#     secret_r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captchadata)
#     response = json.loads(secret_r.text)
#     verify = response.get("success", False)

#     if not verify:
#         return HttpResponse("Please verify that you are not a robot")

#     try:
#         user_report = UserReport.objects.get(user_token__token1=token)

#         # Create a BytesIO buffer to receive the PDF data.
#         buffer = BytesIO()

#         # Create the PDF object, using the BytesIO buffer as its "file."
#         doc = SimpleDocTemplate(buffer, pagesize=letter)

#         # Create a list to hold the flowables, which will be added to the PDF.
#         elements = []

#         # Clinic name (top left)
#         clinic_name_style = ParagraphStyle(name="ClinicName", fontSize=12, alignment=0)
#         clinic_name_text = Paragraph(user_report.clinic_name, clinic_name_style)
#         elements.append(clinic_name_text)

#         # Current datetime (top right)
#         current_datetime = user_report.date.strftime("%Y-%m-%d %H:%M:%S")
#         current_datetime_style = ParagraphStyle(name="CurrentDatetime", fontSize=10, alignment=2)
#         current_datetime_text = Paragraph(current_datetime, current_datetime_style)
#         elements.append(current_datetime_text)

#         # Add a horizontal line below clinic name and date
#         elements.append(HRFlowable(width="100%", color=colors.black, thickness=1, spaceBefore=6, spaceAfter=6))

#         # User email
#         user_email_style = ParagraphStyle(name="UserEmail", fontSize=8)
#         user_email_text = Paragraph(f"Email: {user_report.email}", user_email_style)
#         elements.append(user_email_text)

#         # Add some space
#         elements.append(Spacer(1, 14))

#         # Split the report text into paragraphs
#         report_text = user_report.report
#         report_paragraphs = report_text.split('\n')  # Split on newlines for example

#         # Create ParagraphStyle for report text
#         report_text_style = getSampleStyleSheet()["Normal"]

#         # Create separate Paragraphs for each part of the report
#         for part in report_paragraphs:
#             report_paragraph = Paragraph(part, report_text_style)
#             elements.append(report_paragraph)
#             elements.append(Spacer(1, 5)) 

#         # Add some space
#         elements.append(Spacer(1, 12))

#         # Thank you message with font size 10
#         thank_you_style = ParagraphStyle(name="ThankYou", fontSize=10, textColor=colors.green)
#         thank_you_text = Paragraph("Thank you!", thank_you_style)
#         elements.append(thank_you_text)

#         # Build the PDF document and close the buffer.
#         doc.build(elements)
#         buffer.seek(0)

#         # Create a Django HttpResponse to send the PDF as a download.
#         response = HttpResponse(buffer.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="generated_report.pdf"'

#         return response
#     except Exception as e:
#         return HttpResponse(f"Problem :: {e}")
    
    
    
#     import os
# import random
# from PIL import Image, ImageDraw, ImageFont  # Import ImageFont
# from django.http import (
#     HttpResponseBadRequest,
#     HttpResponseServerError,
#     JsonResponse,
#     HttpResponse,
# )
# from django.utils import timezone
# from django.shortcuts import redirect, render
# from roboflow import Roboflow
# from ai755 import settings
# import datetime
# from ai75589674.pdf_generator import generate_dental_report
# from ai75589674.models import *
# import requests
# import json
# from django.core.files.storage import default_storage

# import supervision as sv
# import cv2

# # PDF IMPORTS
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.core.exceptions import ObjectDoesNotExist
# from django.shortcuts import render
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
# from reportlab.lib.styles import getSampleStyleSheet
# from io import BytesIO


# # MAIN PAGE
# def result_pg_rendering(request):
#     return render(request, "ai75589674/result1.html")


# def confirmation_page(request):
#     return render(request, "ai75589674/result2.html")


# def about(request):
#     return render(request, "ai75589674/about.html")


# def privacy(request):
#     return render(request, "ai75589674/trems_and_conditions.html")


# def conatctus(request):
#     try:
#         if request.method == "POST":
#             # GETTING
#             f_name = request.POST.get("fname")
#             lname = request.POST.get("lname")
#             email = request.POST.get("email")
#             phno = request.POST.get("phno")
#             Subject = request.POST.get("Subject")
#             umsg = request.POST.get("umsg")
#             job = request.POST.get("job")

#         else:
#             return render(request, "ai75589674/contact.html")
#     except:
#         return HttpResponseBadRequest("Not a Post.")


# def generate_pdf(request):
#     if request.method != "POST":
#         return HttpResponseBadRequest("Bad request")

#     token = request.POST.get("token")

#     try:
#         # Check if the user with the provided token exists
#         user_report = UserReport.objects.get(user_token__token1=token)

#     except ObjectDoesNotExist:
    
#         return HttpResponseBadRequest("Please upload your image")

#     grr = request.POST.get("g-recaptcha-response")

#     sscptcha = settings.captcha_site_key

#     captchadata = {"secret": sscptcha, "response": grr}
#     secret_r = requests.post(
#         "https://www.google.com/recaptcha/api/siteverify", data=captchadata
#     )
#     response = json.loads(secret_r.text)
#     verify = response.get("success", False)

#     if not verify:
#         return HttpResponseBadRequest("Please verify that you are not a robot")

#     try:
#         # Create a BytesIO buffer to receive the PDF data.
#         buffer = BytesIO()

#         # Create the PDF object, using the BytesIO buffer as its "file."
#         doc = SimpleDocTemplate(buffer, pagesize=letter)

#         # Create a list to hold the flowables, which will be added to the PDF.
#         elements = []

#         # Clinic name (top left)
#         clinic_name_style = ParagraphStyle(name="ClinicName", fontSize=12, alignment=0)
#         clinic_name_text = Paragraph(user_report.clinic_name, clinic_name_style)
#         elements.append(clinic_name_text)

#         # Current datetime (top right)
#         current_datetime = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
#         current_datetime_style = ParagraphStyle(
#             name="CurrentDatetime", fontSize=10, alignment=2
#         )
#         current_datetime_text = Paragraph(current_datetime, current_datetime_style)
#         elements.append(current_datetime_text)

#         # Add a horizontal line below clinic name and date
#         elements.append(
#             HRFlowable(
#                 width="100%",
#                 color=colors.black,
#                 thickness=1,
#                 spaceBefore=6,
#                 spaceAfter=6,
#             )
#         )

#         # User email
#         user_email_style = ParagraphStyle(name="UserEmail", fontSize=8)
#         user_email_text = Paragraph(f"Email: {user_report.email}", user_email_style)
#         elements.append(user_email_text)

#         # Add some space
#         elements.append(Spacer(1, 14))

#         # Split the report text into paragraphs
#         report_text = user_report.report
#         report_paragraphs = report_text.split("\n")  # Split on newlines for example

#         # Create ParagraphStyle for report text
#         report_text_style = getSampleStyleSheet()["Normal"]

#         # Create separate Paragraphs for each part of the report
#         for part in report_paragraphs:
#             report_paragraph = Paragraph(part, report_text_style)
#             elements.append(report_paragraph)
#             elements.append(Spacer(1, 5))

#         # Add some space
#         elements.append(Spacer(1, 12))

#         # Thank you message with font size 10
#         thank_you_style = ParagraphStyle(
#             name="ThankYou", fontSize=10, textColor=colors.green
#         )
#         thank_you_text = Paragraph("Thank you!", thank_you_style)
#         elements.append(thank_you_text)

#         # Build the PDF document and close the buffer.
#         doc.build(elements)
#         buffer.seek(0)
#         file_datetime = timezone.now().strftime("%Y-%m-%d %H_%M_%S")
#         # Define the file path where you want to save the PDF.
#         pdf_file_path = f"reports/{file_datetime}-{random.randint(500, 5000)}.pdf"

#         # Save the PDF to the specified path using Django's default_storage.
#         with default_storage.open(pdf_file_path, "wb") as pdf_file:
#             pdf_file.write(buffer.read())
        
#         email_content = render_to_string('ai75589674/email/email.html', {'report_url': f"/media/{pdf_file_path}"})
#         email = EmailMessage(
#         subject='Your Medical Report PDF',
#         body=email_content,  # Use the rendered email template
#         from_email=settings.EMAIL_HOST_USER,
#         to=[user_report.email],
#          )
#         email.content_subtype = "html"
#         email.send()
#         response_data = {"message": "Report has been sent successfully."}
#         return JsonResponse(response_data, safe=False)  # Set safe=False
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, safe=False)


# def prevent_overlap(labels, position, label_size, vertical_spacing=60):
#     try:
#         x1, y1, x2, y2 = (
#             position[0] - label_size[0] / 2,
#             position[1],
#             position[0] + label_size[0] / 2,
#             position[1] + label_size[1],
#         )
#         for existing_position, existing_size in labels:
#             ex1, ey1, ex2, ey2 = (
#                 existing_position[0] - existing_size[0] / 2,
#                 existing_position[1],
#                 existing_position[0] + existing_size[0] / 2,
#                 existing_position[1] + existing_size[1],
#             )
#             if (
#                 x1 < ex2
#                 and x2 > ex1
#                 and y1 < ey2 + vertical_spacing
#                 and y2 > ey1 - vertical_spacing
#             ):
#                 position = (position[0], ey1 - vertical_spacing - label_size[1])
#         return position
#     except Exception as e:
#         return JsonResponse({"error": e})


# def process_image(image_path, predictions):
#     try:
#         image = Image.open(image_path)
#         image_pil = image.convert("RGB")
#         draw = ImageDraw.Draw(image_pil)
#         highlight_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
#         font = ImageFont.truetype("arial.ttf", 14)
#         label_positions = []

#         for i, bounding_box in enumerate(predictions["predictions"]):
#             points = [
#                 (
#                     bounding_box["x"] - bounding_box["width"] / 2,
#                     bounding_box["y"] - bounding_box["height"] / 2,
#                 ),
#                 (
#                     bounding_box["x"] + bounding_box["width"] / 2,
#                     bounding_box["y"] - bounding_box["height"] / 2,
#                 ),
#                 (
#                     bounding_box["x"] + bounding_box["width"] / 2,
#                     bounding_box["y"] + bounding_box["height"] / 2,
#                 ),
#                 (
#                     bounding_box["x"] - bounding_box["width"] / 2,
#                     bounding_box["y"] + bounding_box["height"] / 2,
#                 ),
#             ]
#             color = highlight_colors[i % len(highlight_colors)]
#             draw.polygon(points, outline=color, width=2)

#             label_text = bounding_box["class"]
#             label_size = draw.textsize(
#                 label_text, font=font
#             )  # Use draw.textsize to get the text size
#             label_position = (
#                 int(bounding_box["x"]),
#                 int(bounding_box["y"] - bounding_box["height"] / 2) - label_size[1],
#             )
#             label_position = prevent_overlap(
#                 label_positions, label_position, label_size
#             )
#             label_positions.append((label_position, label_size))
#             label_background = (
#                 label_position[0],
#                 label_position[1],
#                 label_position[0] + label_size[0] + 10,
#                 label_position[1] + label_size[1] + 10,
#             )
#             draw.rectangle(label_background, fill=color)
#             bold_font = ImageFont.truetype("arialbd.ttf", 14)
#             draw.text(
#                 (label_position[0] + 2, label_position[1] + 2),
#                 label_text,
#                 fill=(0, 0, 0),
#                 font=bold_font,
#             )

#         return image_pil
#     except Exception as e:
#         return JsonResponse({"error": e})


# """
# BackupDoc ai Property
# """


# def result(request):
#     try:
#         if request.method == "POST":
#             try:
#                 image_path = request.FILES.get("file")
#                 confidence = request.POST.get("myrange")
#                 email = request.POST.get("email")
#                 grr = request.POST.get("g-recaptcha-response")

#                 # Check if the Recaptcha response is empty or not
#                 if not grr:
#                     return JsonResponse({"error": "Captcha Failed"})

#                 sscptcha = settings.captcha_site_key

#                 captchadata = {"secret": sscptcha, "response": grr}
#                 secret_r = requests.post(
#                     "https://www.google.com/recaptcha/api/siteverify", data=captchadata
#                 )
#                 response = json.loads(secret_r.text)

#                 verify = response["success"]

#                 if verify:
#                     try:
#                         upload_path = os.path.join(
#                             settings.MEDIA_ROOT, "temp", image_path.name
#                         )
#                         with open(upload_path, "wb+") as destination:
#                             for chunk in image_path.chunks():
#                                 destination.write(chunk)
#                         rf = Roboflow(api_key=settings.ROBO_API_KEY)
#                         project = rf.workspace().project("doclabs")
#                         model = project.version(2).model
#                         prediction = model.predict(
#                             upload_path, confidence=confidence
#                         ).json()
#                         image_pil = process_image(upload_path, prediction)
#                         # Generate a random filename for the analyzed image
#                         current_datetime = datetime.datetime.now().strftime(
#                             "%Y%m%d%H%M%S"
#                         )
#                         random_number = random.randint(1000, 9999)
#                         random_filename = (
#                             f"{current_datetime}-{random_number}" + ".jpeg"
#                         )
#                         output_image_path = os.path.join(
#                             settings.MEDIA_ROOT, "analyzed", random_filename
#                         )
#                         # Save the image to the output path
#                         image_pil.save(output_image_path, "JPEG")
#                         token = f"dnwedasdsdfewr{random.randint(100,999)}adiwefbneriufb{random.randint(10,99)}"
#                         ch = Black_token(token1=token)
#                         ch.save()
#                         generate_dental_report(prediction, token, email)
#                         # Define the URL for the saved image
#                         analyzed_image_url = f"/media/analyzed/{random_filename}"  # Update the path as needed

#                         content = {
#                             "session_token": token,
#                             "url": analyzed_image_url,
#                             "opt_url": upload_path,
#                         }
#                         return JsonResponse(content)
#                     except Exception as e:
#                         return JsonResponse(
#                             {"error": "Something went wrong, Please try again"}
#                         )
#                 else:
#                     return JsonResponse({"error": "Recaptcha Failed"})

#             except FileNotFoundError as e:
#                 return JsonResponse({"error": "File Not Found"})

#         # For GET requests, don't process the form data again
#         elif request.method == "GET":
#             return JsonResponse({"error": "BAD REQUEST"})

#         else:
#             return JsonResponse({"error": "Bad Request"})

#     except Exception as e:
#         return JsonResponse({"error": "SERVER ERROR!"})


# def reanalyze(request):
#     try:
#         if request.method == "POST":
#             image = request.POST.get("file")
#             confidence = request.POST.get("confidence")
#             token = request.POST.get("token")

#             # Fetch the user's email from the database based on the token
#             user_email = UserReport.objects.filter(user_token__token1=token).first()
#             if user_email:
#                 email = user_email.email
#             else:
#                 email = None  # Set a default value if the user is not found

#             rf = Roboflow(api_key=settings.ROBO_API_KEY)
#             project = rf.workspace().project("stage-1-launch")
#             model = project.version(1).model
#             prediction = model.predict(image, confidence=confidence).json()

#             image_pil = process_image(image, prediction)
#             current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#             random_number = random.randint(1000, 9999)
#             random_filename = f"{current_datetime}-{random_number}" + ".jpeg"
#             output_image_path = os.path.join(
#                 settings.MEDIA_ROOT, "analyzed", random_filename
#             )
#             image_pil.save(output_image_path, "JPEG")
#             generate_dental_report(prediction, token, email)
#             analyzed_image_url = (
#                 f"/media/analyzed/{random_filename}"  # Update the path as needed
#             )

#             content = {
#                 "url": analyzed_image_url,
#                 # Other data you want to include in the response
#             }

#             return JsonResponse(content)
#     except Exception as e:
#         return JsonResponse(e)
# # def prevent_overlap(labels, position, label_size, vertical_spacing=60):
# #     try:
# #         x1, y1, x2, y2 = (
# #             position[0] - label_size[0] / 2,
# #             position[1],
# #             position[0] + label_size[0] / 2,
# #             position[1] + label_size[1],
# #         )
# #         for existing_position, existing_size in labels:
# #             ex1, ey1, ex2, ey2 = (
# #                 existing_position[0] - existing_size[0] / 2,
# #                 existing_position[1],
# #                 existing_position[0] + existing_size[0] / 2,
# #                 existing_position[1] + existing_size[1],
# #             )
# #             if (
# #                 x1 < ex2
# #                 and x2 > ex1
# #                 and y1 < ey2 + vertical_spacing
# #                 and y2 > ey1 - vertical_spacing
# #             ):
# #                 position = (position[0], ey1 - vertical_spacing - label_size[1])
# #         return position
# #     except Exception as e:
# #         return JsonResponse({"error": e})

# # def process_image(image_path, predictions):
# #     try:
# #         image = Image.open(image_path)
# #         image_pil = image.convert("RGB")
# #         draw = ImageDraw.Draw(image_pil)
# #         highlight_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
# #         font = ImageFont.truetype("arial.ttf", 14)
# #         label_positions = []

# #         for i, bounding_box in enumerate(predictions["predictions"]):
# #             points = [
# #                 (
# #                     bounding_box["x"] - bounding_box["width"] / 2,
# #                     bounding_box["y"] - bounding_box["height"] / 2,
# #                 ),
# #                 (
# #                     bounding_box["x"] + bounding_box["width"] / 2,
# #                     bounding_box["y"] - bounding_box["height"] / 2,
# #                 ),
# #                 (
# #                     bounding_box["x"] + bounding_box["width"] / 2,
# #                     bounding_box["y"] + bounding_box["height"] / 2,
# #                 ),
# #                 (
# #                     bounding_box["x"] - bounding_box["width"] / 2,
# #                     bounding_box["y"] + bounding_box["height"] / 2,
# #                 ),
# #             ]
# #             color = highlight_colors[i % len(highlight_colors)]
# #             draw.polygon(points, outline=color, width=2)

# #             label_text = bounding_box["class"]
# #             label_size = draw.textsize(
# #                 label_text, font=font
# #             )  # Use draw.textsize to get the text size
# #             label_position = (
# #                 int(bounding_box["x"]),
# #                 int(bounding_box["y"] - bounding_box["height"] / 2) - label_size[1],
# #             )
# #             label_position = prevent_overlap(
# #                 label_positions, label_position, label_size
# #             )
# #             label_positions.append((label_position, label_size))
# #             label_background = (
# #                 label_position[0],
# #                 label_position[1],
# #                 label_position[0] + label_size[0] + 10,
# #                 label_position[1] + label_size[1] + 10,
# #             )
# #             draw.rectangle(label_background, fill=color)
# #             bold_font = ImageFont.truetype("arialbd.ttf", 14)
# #             draw.text(
# #                 (label_position[0] + 2, label_position[1] + 2),
# #                 label_text,
# #                 fill=(0, 0, 0),
# #                 font=bold_font,
# #             )

# #         return image_pil
# #     except Exception as e:
# #         return JsonResponse({"error": e})