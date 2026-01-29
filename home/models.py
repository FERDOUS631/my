from pydoc import text
import uuid
from django.db import models

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Notice(models.Model):
    sl = models.CharField(max_length=10)
    date = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='file/notices/', null=True, blank=True,max_length=500 )


    def __str__(self):
        return self.subject

# student result model
# models.py

def result_pdf_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"result_pdfs/{uuid.uuid4()}.{ext}"

class ResultPDF(models.Model):
    pdf = models.FileField(upload_to="results_pdfs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class StudentResult(models.Model):
    roll = models.IntegerField(unique=True)
    gpa1 = models.CharField(max_length=10, null=True, blank=True)
    gpa2 = models.CharField(max_length=10, null=True, blank=True)
    gpa3 = models.CharField(max_length=10, null=True, blank=True)
    gpa4 = models.CharField(max_length=10, null=True, blank=True)
    gpa5 = models.CharField(max_length=10, null=True, blank=True)
    gpa6 = models.CharField(max_length=10, null=True, blank=True)
    gpa7 = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.roll)

class Headline(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text
    
class Phone_Email(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Phone: {self.phone}, Email: {self.email}"