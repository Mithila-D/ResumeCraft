from django import forms

class ResumeForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone Number', max_length=15)
    skills = forms.CharField(label='Adress', widget=forms.Textarea)
    # image = forms.ImageField(label='Upload Photo', required=False)
    experience = forms.CharField(label='Experience', widget=forms.Textarea, required=False)
    certifications = forms.CharField(label='Certifications', widget=forms.Textarea, required=False)
    education = forms.CharField(label='Education', widget=forms.Textarea, required=False)
    technical_skills = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter technical skills'}), required=False)
    tools_and_libraries = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter tools and libraries'}), required=False)
    soft_skills = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter soft skills'}), required=False)
    achievements = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter achievements'}), required=False)
    job_role = forms.ChoiceField(choices=[('Data Scientist', 'Data Scientist'),
                                          ('Software Developer', 'Software Developer'),
                                          ('Business Analyst', 'Business Analyst'),
                                          ('Front-End Developer', 'Front-End Developer'),
                                          ('Full-Stack Developer', 'Full-Stack Developer')])
    experience_level = forms.ChoiceField(choices=[('fresher', 'Fresher'), ('experienced', 'Experienced')])
from django import forms



