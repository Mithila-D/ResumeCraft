from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home, name='home'),
    path('form/', views.form_view, name='form_view'),
    path('resume/', views.resume_view, name='resume_view'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'), 
    path('signin/', views.login_view, name='signin'),  
    path('signup/', views.signup_view, name='signup'),
    path('form2/', views.submit_form, name='submit_form'),
    
    path('resume2/', views.resume2, name='resume2'), 
    path('resume3/', views.resume3, name='resume3'), 
    path('generate_pdf_resume3/', views.generate_pdf_resume3, name='generate_pdf_resume3'), 
    
    path('choose/', views.choose_template, name='choose'), 
    path('manual/', views.manual, name='manual'), 
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
