
from django.urls import path
from .views import *
urlpatterns = [
   
    path('lab', result, name="Lab"),
    path('lab-demo', demo_page_lab, name="Demo_page_lab"),
    path('demo', demo_page, name="Lab"),
    #path('rlab', reanalyze, name="RLab"),
    path('about', about, name="a-bout"),
    path('privacy', privacy, name="Privacy"),
    path('contact', conatctus, name="Conatctus"),
    path('r-generate_report', generate_pdf, name='generate_pdf'),
    path('analysis', confirmation_page, name="confirmation-page"),
    path('up-handle', result_pg_rendering, name="Up-Handle"),
    path('demo-me', demo, name="Demo"),
    
]