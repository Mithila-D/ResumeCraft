from django import forms
from django.shortcuts import render
from .forms import ResumeForm
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string




 
def form_view(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid(): 
            name_corrected, name_errors = check_spelling(form.cleaned_data['name'])
            email_corrected, email_errors = check_spelling(form.cleaned_data['email'])
            phone_corrected, phone_errors = check_spelling(form.cleaned_data['phone'])
            skills_corrected, skills_errors = check_spelling(form.cleaned_data['skills'])
            experience_corrected, experience_errors = check_spelling(form.cleaned_data['experience'])
            certifications_corrected, certifications_errors = check_spelling(form.cleaned_data['certifications'])
            education_corrected, education_errors = check_spelling(form.cleaned_data['education'])
             
            all_errors = name_errors + email_errors + phone_errors + skills_errors + experience_errors + certifications_errors + education_errors
            
            if all_errors:
                return render(request, 'resume/form.html', {
                    'form': form,
                    'errors': all_errors  
                })
            else:
                request.session['resume_data'] = {
                    'name': name_corrected,
                    'email': email_corrected,
                    'phone': phone_corrected,
                    'skills': skills_corrected,
                    'experience': experience_corrected,
                    'certifications': certifications_corrected,
                    'education': education_corrected,
                }
                return render(request, 'resume/resume.html', {'form': request.session['resume_data']})

    else:
        form = ResumeForm()  
    
    return render(request, 'resume/form.html', {'form': form})

from django.shortcuts import render
from .forms import ResumeForm
def resume_view(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)  
        if form.is_valid():
            # image = form.cleaned_data.get('image')  
            # if image:
            #     print(f"Image uploaded: {image.name}")  
            # else:
            #     print("No image uploaded.")
            resume_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'skills': form.cleaned_data['skills'],
                'experience': form.cleaned_data['experience'],
                'certifications': form.cleaned_data['certifications'],
                'education': form.cleaned_data['education'],
            }

            return render(request, 'resume/resume.html', {'form': resume_data}) 
    else:
        form = ResumeForm()  
    return render(request, 'resume/form.html', {'form': form}) 

def Home(request):
    return render(request, 'resume/Home.html')


def generate_pdf(request):
    resume_data = request.session.get('resume_data', {})
     
    html_content = render_to_string('resume/resume.html', {'form': resume_data})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    HTML(string=html_content).write_pdf(response)
    
    return response


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User 
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

def signup_view(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        if User.objects.filter(UserName=UserName).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
            return redirect('signup')  
        try:
            hashed_password = make_password(Password)
            user = User(UserName=UserName, Password=hashed_password)
            user.save()
            messages.success(request, 'User registered successfully. You can now log in.')
            return redirect('signin')  
        except IntegrityError:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return redirect('signup') 
    return render(request, 'resume/SignUp.html') 

def login_view(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Password = request.POST.get('Password')
        try:
            user = User.objects.get(UserName=UserName)
            if check_password(Password, user.Password):
                return redirect('choose')  
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, 'User not found or incorrect credentials.')
            return redirect('signin')
    return render(request, 'resume/SignIn.html')  







def choose_template(request):
    return render(request, 'resume/choose.html')



def manual(request):
    return render(request, 'resume/manual.html')





#---------------------------------------------------------------------------------------------------


from django.shortcuts import render
from django.http import HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

job_keywords = {
    "Data Scientist": {
        "technical_skills": [
            "data analysis", "machine learning", "statistics", "big data", "predictive modeling",
            "data visualization", "deep learning", "NLP", "data wrangling", "data mining"
        ],
        "tools_and_libraries": [
            "Python", "R", "SQL", "TensorFlow", "Keras", "scikit-learn", "Apache Spark",
            "Hadoop", "Pandas", "NumPy", "Jupyter Notebook", "Tableau", "Power BI", "D3.js"
        ],
        "soft_skills": [
            "critical thinking", "problem-solving", "attention to detail", "communication",
            "collaboration", "adaptability", "analytical mindset", "continuous learning"
        ],
        "achievements": [
            "published research", "data competition participation", "ML model deployment",
            "patent contributions", "conference presentations", "top Kaggle scores"
        ]
    },
    "Software Developer": {
        "technical_skills": [
            "coding", "algorithms", "debugging", "object-oriented programming", "problem-solving",
            "testing", "optimization", "scalability", "performance tuning"
        ],
        "tools_and_libraries": [
            "JavaScript", "Python", "C++", "Java", "SQL", "Git", "Docker", "Kubernetes",
            "Jenkins", "REST APIs", "Spring", "Django", "Node.js", "React", "Angular", "AWS"
        ],
        "soft_skills": [
            "teamwork", "time management", "communication", "attention to detail", "creativity",
            "adaptability", "collaborative mindset", "continuous improvement"
        ],
        "achievements": [
            "open-source contributions", "hackathon participation", "certifications",
            "side projects", "personal portfolio", "technical leadership"
        ]
    },
    "Business Analyst": {
        "technical_skills": [
            "analytics", "data visualization", "stakeholder engagement", "problem-solving",
            "requirement analysis", "project management", "reporting", "business case development"
        ],
        "tools_and_libraries": [
            "Excel", "Power BI", "SQL", "Tableau", "Jira", "Confluence", "Microsoft Project",
            "Visio", "Google Analytics", "SPSS", "SAS", "Qlik"
        ],
        "soft_skills": [
            "analytical thinking", "communication", "stakeholder management", "adaptability",
            "strategic thinking", "negotiation", "presentation skills"
        ],
        "achievements": [
            "project completions", "certifications in business analysis", "recognition awards",
            "process improvements", "successful project delivery"
        ]
    },
    "Front-End Developer": {
        "technical_skills": [
            "HTML", "CSS", "JavaScript", "user interface design", "responsive design", "UX/UI",
            "SEO", "web accessibility", "cross-browser compatibility", "user-centric design"
        ],
        "tools_and_libraries": [
            "React", "Vue.js", "Angular", "Bootstrap", "Sass", "Figma", "Sketch",
            "Adobe XD", "Webpack", "Babel", "Git", "Photoshop", "Illustrator"
        ],
        "soft_skills": [
            "creativity", "attention to detail", "communication", "adaptability", "problem-solving",
            "time management"
        ],
        "achievements": [
            "portfolio of design projects", "successful website launches", "UI/UX certifications",
            "contributions to design systems", "recognition for design aesthetics"
        ]
    },
    "Full-Stack Developer": {
        "technical_skills": [
            "full-stack development", "RESTful APIs", "database management", "cloud computing",
            "server-side programming", "web security", "scalability"
        ],
        "tools_and_libraries": [
            "JavaScript", "Node.js", "React", "Express", "MongoDB", "PostgreSQL", "MySQL",
            "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "Git", "GraphQL", "TypeScript"
        ],
        "soft_skills": [
            "problem-solving", "adaptability", "collaboration", "communication", "time management",
            "attention to detail"
        ],
        "achievements": [
            "successful app deployments", "cross-functional project work", "API integration projects",
            "certifications in full-stack development", "open-source contributions"
        ]
    }
}

experience_keywords = {
    "fresher": [
        "internships", "certifications", "volunteering", "academic projects", "team player",
        "eager to learn", "entry-level", "basic knowledge", "enthusiasm", "foundation skills"
    ],
    "experienced": [
        "leadership", "project management", "mentorship", "senior roles", "specialization",
        "expertise", "results-oriented", "strategy", "advanced skills", "problem-solving at scale"
    ]
}



from django.shortcuts import render
from .forms import ResumeForm
# from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import match_keywords, check_spelling










from django.shortcuts import render
from .forms import ResumeForm
from .utils import match_keywords, check_spelling

def submit_form(request):
   
    feedback = {
        'missing_skills': [],
        'spelling_errors': []
    }
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)  
        if form.is_valid():  
            user_data = form.cleaned_data
            
            job_role = user_data.get("job_role")
            experience_level = user_data.get("experience_level")
            technical_skills = user_data.get('technical_skills', '')
            tools_and_libraries = user_data.get('tools_and_libraries', '')
            soft_skills = user_data.get('soft_skills', '')
            achievements = user_data.get('achievements', '')
            
            print("Submitted Skills:", technical_skills)
            
            # Identify missing skills based on job role and experience level
            feedback['missing_skills'] = match_keywords(user_data, job_role, experience_level)
            
            # Process sections for spelling errors
            for section in ['technical_skills', 'soft_skills']:
                section_content = user_data.get(section)
                if section_content:  
                    # Convert lists to strings
                    if isinstance(section_content, list):
                        section_content = " ".join(section_content)
                    corrected_text, errors = check_spelling(section_content)
                    feedback['spelling_errors'] += errors
             
            return render(request, 'resume/form2.html', {'form': form, 'feedback': feedback})
    
    # Handle GET request: render an empty form
    else:
        form = ResumeForm()
    
    # Render the form with initial empty feedback
    return render(request, 'resume/form2.html', {'form': form, 'feedback': feedback})

























from django.shortcuts import render
from .forms import ResumeForm

def resume2(request):
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
         
        if form.is_valid():
        
            return render(request, 'resume/resume2.html', {'form': form})
 
    else:
        form = ResumeForm()

    return render(request, 'resume/resume2.html', {'form': form})







from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResumeForm
from weasyprint import HTML
from django.template.loader import render_to_string

def resume3(request):
    form = ResumeForm(request.POST or None)
     
    technical_skills_list = []
    tools_and_libraries_list = []
    
    if form.is_valid():
        # Store the form data in the session for PDF generation later
        request.session['resume_data'] = form.cleaned_data
         
        technical_skills = form.cleaned_data.get('technical_skills', '')
        tools_and_libraries = form.cleaned_data.get('tools_and_libraries', '')
        
        # Split skills and tools into lists
        technical_skills_list = [skill.strip() for skill in technical_skills.split(',')] if technical_skills else []
        tools_and_libraries_list = [tool.strip() for tool in tools_and_libraries.split(',')] if tools_and_libraries else []
        print("Technical Skills:", technical_skills_list)  
 
    return render(request, 'resume/resume3.html', {
        'form': form,
        'technical_skills_list': technical_skills_list,
        'tools_and_libraries_list': tools_and_libraries_list,
    })







































def generate_pdf_resume3(request):
   
    resume_data = request.session.get('resume_data', None)
    
    if not resume_data:
        return HttpResponse("No resume data found.", status=400)

    
    
    
    name = resume_data.get('name', '')
    phone=resume_data.get('phone','')
    email=resume_data.get('email','')
    education=resume_data.get('education','')
    job_role=resume_data.get('job_role','')
    soft_skills=resume_data.get('soft_skills','')
    education=resume_data.get('education','')
    achievements=resume_data.get('achievements','')
    skills=resume_data.get('skills','')
    experience_level=resume_data.get('experience_level','')
    experience=resume_data.get('experience','')
    certifications=resume_data.get('certifications','')
    
    
    
     
    technical_skills = resume_data.get('technical_skills', '')
    tools_and_libraries = resume_data.get('tools_and_libraries', '')
     
    technical_skills_list = technical_skills.split(',') if technical_skills else []
    tools_and_libraries_list = tools_and_libraries.split(',') if tools_and_libraries else []
 
    context = {
        'form': resume_data,   
        'technical_skills_list': technical_skills_list,
        'tools_and_libraries_list': tools_and_libraries_list,
        'name': name,
        'phone': phone,
        'email': email,
        'education': education,
        'job_role': job_role,
        'soft_skills': soft_skills,
        'achievements': achievements,
        'skills': skills,
        'experience_level': experience_level,
        'experience': experience,
        'certifications': certifications,
    }
 
    print("Context Data for PDF Rendering:", context)
    
 
    html_content = render_to_string('resume/resume3.html', context)
    print(html_content)
  
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume3.pdf"'

    HTML(string=html_content).write_pdf(response)
    
    return response
