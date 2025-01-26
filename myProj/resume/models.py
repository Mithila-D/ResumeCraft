from django.db import models

class User(models.Model):
    UserName = models.CharField(max_length=255, unique=True)
    Password = models.CharField(max_length=255) 

    def __str__(self):
        return self.UserName



from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    skills = models.TextField()
    experience = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    education = models.TextField(blank=True)
    technical_skills = models.TextField(blank=True)
    tools_and_libraries = models.TextField(blank=True)
    soft_skills = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    job_role = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=20)

    def __str__(self):
        return self.name
