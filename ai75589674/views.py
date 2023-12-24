from __future__ import print_function
import os
import random
from PIL import Image
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.shortcuts import redirect, render
from roboflow import Roboflow
from ai755 import settings
import datetime
from ai75589674.pdf_generator import generate_dental_report
from ai75589674.models import *
import requests
import json
from django.core.files.storage import default_storage

from email.mime.base import MIMEBase
from email import encoders

import supervision as sv
import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PDF IMPORTS

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from controler.models import *
from .email_manager import email_sender
from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger(__name__)


# MAIN PAGE
@csrf_exempt
def result_pg_rendering(request):
    return render(request, "ai75589674/result1.html")


def confirmation_page(request):
    return render(request, "ai75589674/result2.html")


def demo(request):
    return render(request, "ai75589674/demo1.html")


def demo_page(request):
    return render(request, "ai75589674/demo.html")


def about(request):
    about_data = About_Page.objects.get(id=1)
    content = {"about_data": about_data}
    return render(request, "ai75589674/about.html", content)


def privacy(request):
    privacy_data = Privacy_Edit.objects.get(id=1)
    content = {"privacy_data": privacy_data}
    return render(request, "ai75589674/trems_and_conditions.html", content)


@csrf_exempt
def conatctus(request):
    try:
        if request.method == "POST":
            # GETTING
            f_name = request.POST.get("fname")
            lname = request.POST.get("lname")
            email = request.POST.get("email")
            phno = request.POST.get("phno")
            Subject = request.POST.get("Subject")
            umsg = request.POST.get("umsg")
            job = request.POST.get("job")

            user_msg = contact(
                first_name=f_name,
                last_name=lname,
                email=email,
                phone_no=phno,
                message=umsg,
                job_title=job,
                subject=Subject,
            )

            user_msg.save()

            return redirect("Conatctus")

        else:
            return render(request, "ai75589674/contact.html")
    except:
        return HttpResponseBadRequest("Not a Post.")


@csrf_exempt
def generate_pdf(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Bad request")

    token = request.POST.get("token")

    try:
        # Check if the user with the provided token exists
        user_report = UserReport.objects.get(user_token__token1=token)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Please upload your image")

    grr = request.POST.get("g-recaptcha-response")
    sscptcha = settings.captcha_site_key
    captchadata = {"secret": sscptcha, "response": grr}
    secret_r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=captchadata
    )
    response = json.loads(secret_r.text)
    verify = response.get("success", False)

    if not verify:
        return HttpResponseBadRequest("Please verify that you are not a robot")

    try:
        # Create a BytesIO buffer to receive the PDF data.
        buffer = BytesIO()

        # Create the PDF object, using the BytesIO buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Create a list to hold the flowables, which will be added to the PDF.
        elements = []

        # Clinic name (top left)
        clinic_name_style = ParagraphStyle(name="ClinicName", fontSize=12, alignment=0)
        clinic_name_text = Paragraph(user_report.clinic_name, clinic_name_style)
        elements.append(clinic_name_text)

        # Current datetime (top right)
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        current_datetime_style = ParagraphStyle(
            name="CurrentDatetime", fontSize=10, alignment=2
        )
        current_datetime_text = Paragraph(current_datetime, current_datetime_style)
        elements.append(current_datetime_text)

        # Add a horizontal line below clinic name and date
        elements.append(
            HRFlowable(
                width="100%",
                color=colors.black,
                thickness=1,
                spaceBefore=6,
                spaceAfter=6,
            )
        )

        # User email
        user_email_style = ParagraphStyle(name="UserEmail", fontSize=8)
        user_email_text = Paragraph(f"Email: {user_report.email}", user_email_style)
        elements.append(user_email_text)

        # Add some space
        elements.append(Spacer(1, 14))

        # Split the report text into paragraphs
        report_text = user_report.report
        report_paragraphs = report_text.split("\n")  # Split on newlines for example

        # Create ParagraphStyle for report text
        report_text_style = getSampleStyleSheet()["Normal"]

        # Create separate Paragraphs for each part of the report
        for part in report_paragraphs:
            report_paragraph = Paragraph(part, report_text_style)
            elements.append(report_paragraph)
            elements.append(Spacer(1, 5))

        # Add some space
        elements.append(Spacer(1, 12))

        # Thank you message with font size 10
        thank_you_style = ParagraphStyle(
            name="ThankYou", fontSize=10, textColor=colors.green
        )
        thank_you_text = Paragraph("Thank you!", thank_you_style)
        elements.append(thank_you_text)

        # Build the PDF document and close the buffer.
        doc.build(elements)
        buffer.seek(0)

        file_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_filename = f"/home/shanker/shankers/media/reports/{file_datetime}-{random.randint(500, 5000)}.pdf"

        # Save the PDF to the specified path using Django's default_storage.
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(buffer.read())

        # Send the email with the PDF attachment
        email_sender(user_report.email, pdf_filename, user_report.media)

        response_data = {"message": "Report has been sent successfully."}
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False)


@ensure_csrf_cookie
def result(request):
    try:
        if request.method == "POST":
            try:
                image_path = request.FILES.get("file")
                # confidence = request.POST.get("myrange")

                email = request.POST.get("email")
                grr = request.POST.get("g-recaptcha-response")
                # Check if the Recaptcha response is empty or not
                if not grr:
                    return JsonResponse({"error": "Captcha Failed"})

                sscptcha = settings.captcha_site_key

                captchadata = {"secret": sscptcha, "response": grr}
                secret_r = requests.post(
                    "https://www.google.com/recaptcha/api/siteverify", data=captchadata
                )
                response = json.loads(secret_r.text)

                verify = response["success"]

                if verify:
                    try:
                        upload_path = os.path.join(
                            settings.MEDIA_ROOT, "temp", image_path.name
                        )
                        with open(upload_path, "wb+") as destination:
                            for chunk in image_path.chunks():
                                destination.write(chunk)
                        rf = Roboflow(api_key=settings.ROBO_API_KEY)
                        project = rf.workspace().project("stage-1-launch")
                        model = project.version(1).model
                        prediction = model.predict(upload_path, confidence=1).json()

                        # Process and save annotated image
                        labels = [item["class"] for item in prediction["predictions"]]
                        detections = sv.Detections.from_roboflow(prediction)
                        label_annotator = sv.LabelAnnotator()
                        mask_annotator = sv.MaskAnnotator()
                        image = cv2.imread(upload_path)
                        annotated_image = mask_annotator.annotate(
                            scene=image, detections=detections
                        )
                        annotated_image = label_annotator.annotate(
                            scene=annotated_image, detections=detections, labels=labels
                        )
                        sv.plot_image(image=annotated_image, size=(16, 16))
                        # Convert the NumPy array to a PIL image
                        annotated_image_pil = Image.fromarray(annotated_image)
                        plt.ioff()

                        # Generate a random filename for the analyzed image
                        current_datetime = datetime.datetime.now().strftime(
                            "%Y%m%d%H%M%S"
                        )
                        random_number = random.randint(1000, 9999)
                        random_filename = (
                            f"{current_datetime}-{random_number}" + ".jpeg"
                        )

                        # Define the URL for the saved image
                        analyzed_image_url = f"/media/analyzed/{random_filename}"  # Update the path as needed
                        next_phase = f"/media/temp/{image_path.name}"
                        # Save the annotated image to the output path
                        output_image_path = os.path.join(
                            settings.MEDIA_ROOT, "analyzed", random_filename
                        )

                        annotated_image_pil.save(output_image_path)

                        token = f"dnwedasdsdfewr{random.randint(100,999)}adiwefbneriufb{random.randint(10,99)}"
                        ch = Black_token(token1=token)
                        ch.save()
                        generate_dental_report(
                            prediction, token, email, output_image_path, upload_path
                        )

                        content = {
                            "session_token": token,
                            "url": analyzed_image_url,
                            "opt_url": next_phase,
                        }
                        return JsonResponse(content)
                    except Exception as e:
                        return JsonResponse(
                            {"error": "Something went wrong, Please try again"}
                        )
                else:
                    return JsonResponse({"error": "Captcha Failed"})

            except FileNotFoundError as e:
                return JsonResponse({"error": f"Something went wrong, {e}"})

        # For GET requests, don't process the form data again
        elif request.method == "GET":
            return JsonResponse({"error": "Not a post method BAD REQUEST"})

        else:
            print("bad request")
    except Exception as e:
        return JsonResponse({"error": f"{e}"})


@ensure_csrf_cookie
def demo_page_lab(request):
    try:
        if request.method == "POST":
            try:
                pdf_filename = "/home/shanker/shankers/staticfiles/Assets/data-2.pdf"
                media = "/home/shanker/shankers/staticfiles/Assets/PRE.jpeg"
                email = request.POST.get("email")

                try:
                    email_sender(email, pdf_filename, media)
                    
                    return JsonResponse(
                        {"Success": "Mail sent"}
                    )
                except Exception as e:
                    return JsonResponse(
                        {"error": f"Something went wrong, Please try again {e}"}
                    )
                # else:
                #     return JsonResponse({"error": "Captcha Failed"})

            except FileNotFoundError as e:
                return JsonResponse({"error": f"Something went wrong, {e}"})

        # For GET requests, don't process the form data again
        elif request.method == "GET":
            return JsonResponse({"error": "Not a post method BAD REQUEST"})

        else:
            print("bad request")
    except Exception as e:
        return JsonResponse({"error": f"{e}"})


"""
@csrf_exempt
def reanalyze(request):
    try:
        if request.method == "POST":
            image = request.POST.get("file")
            confidence = request.POST.get("confidence")
            token = request.POST.get("token")

            # Fetch the user's email from the database based on the token
            user_email = UserReport.objects.filter(user_token__token1=token).first()
            if user_email:
                email = user_email.email
            else:
                email = None  # Set a default value if the user is not found

            rf = Roboflow(api_key=settings.ROBO_API_KEY)
            project = rf.workspace().project("stage-1-launch")
            model = project.version(1).model
            prediction = model.predict(image, confidence=confidence).json()
            # Process and save annotated image
            labels = [item["class"] for item in prediction["predictions"]]
            detections = sv.Detections.from_roboflow(prediction)
            label_annotator = sv.LabelAnnotator()
            mask_annotator = sv.MaskAnnotator()
            image = cv2.imread(image)
            annotated_image = mask_annotator.annotate(
                scene=image, detections=detections
            )
            annotated_image = label_annotator.annotate(
                scene=annotated_image, detections=detections, labels=labels
            )
            sv.plot_image(image=annotated_image, size=(12, 12))

            # Convert the NumPy array to a PIL image
            annotated_image_pil = Image.fromarray(annotated_image)
            current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            random_number = random.randint(1000, 9999)
            random_filename = f"{current_datetime}-{random_number}" + ".jpeg"
            output_image_path = os.path.join(
                settings.MEDIA_ROOT, "analyzed", random_filename
            )
            annotated_image_pil.save(output_image_path, "JPEG")
            generate_dental_report(prediction, token, email)
            analyzed_image_url = (
                f"/media/analyzed/{random_filename}"  # Update the path as needed
            )

            content = {
                "url": analyzed_image_url,
                # Other data you want to include in the response
            }

            return JsonResponse(content)
    except Exception as e:
        return JsonResponse(e)
"""
