from .models import Phone_Email, department

def department_list(request):
    departments = department.objects.all()
    phone_email = Phone_Email.objects.all().order_by('-id')
    return {'departments': departments, 'phone_email': phone_email} 