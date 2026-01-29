from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from .models import StudentResult, Notice, Headline, Phone_Email


# Create your views here.
def home(request):
    headlines = Headline.objects.all().order_by('-id')
    context = {'headlines': headlines,}  

    return render(request, 'index.html', context)

def notice_board(request):
    return render(request, 'notice.html')

def notice_api(request):
    notices = Notice.objects.all().order_by('-id')
    notice_list = []

    for n in notices:
        item = {
            'id': n.id,
            'sl': n.sl,
            'date': n.date,
            'department': str(n.department) if n.department else "", 
            'subject': n.subject,
            'author': n.author if n.author else "", 
            'description': n.description if n.description else "",
            'pdf_file': n.pdf_file.url if n.pdf_file else "" 
        }
        notice_list.append(item)

    return JsonResponse(notice_list, safe=False)



def search_result(request):
    if request.method == "POST":
        roll = request.POST.get("roll")
        student = StudentResult.objects.filter(roll=roll).first()
        
        if student:

            request.session['search_result_data'] = {
                'roll': student.roll,
                'gpa1': student.gpa1,
                'gpa2': student.gpa2,
                'gpa3': student.gpa3,
                'gpa4': student.gpa4,
                'gpa5': student.gpa5,
            }
        else:
            request.session['search_result_data'] = "not_found"
       
        return redirect('search_result')

    result = request.session.pop('search_result_data', None)

   
    if result == "not_found":
        return render(request, "result.html", {"error": "Result not found!"})

    return render(request, "result.html", {"result": result})