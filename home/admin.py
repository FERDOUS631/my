from django.contrib import admin
from .utils import extract_results_from_pdf
from .models import Notice, Phone_Email, StudentResult, department,ResultPDF,Headline

# Register your models here.
admin.site.register(department)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('sl', 'date', 'department', 'subject', 'author')
    search_fields = ('sl', 'date', 'department', 'subject', 'author')
   
admin.site.register(Notice, NoticeAdmin)

# Register ResultPDF model and handle PDF processing
@admin.register(ResultPDF)
class ResultPDFAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not obj.pdf:
            return

        results = extract_results_from_pdf(obj.pdf.path)

        if not results:
            self.message_user(request, "⚠ No data extracted from PDF.", level='warning')
            return

        for r in results:
            roll=r.pop("roll")
            StudentResult.objects.update_or_create(
                roll=roll,
                defaults=r
            )
        self.message_user(request, f"✅ Successfully extracted and saved {len(results)} student results.")
         
        


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ("roll", "gpa1", "gpa2", "gpa3", "gpa4", "gpa5")
    search_fields = ("roll",)




# headline admin
@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    
    list_display = ("text",)
    search_fields = ("text",)
    


# phone email admin
@admin.register(Phone_Email)
class PhoneEmailAdmin(admin.ModelAdmin):
    list_display = ("phone", "email")
    search_fields = ("phone", "email")

#administor name tittle chance
admin.site.site_header = "KPI Notice Admin Panel"
admin.site.site_title = "KPI Notice Admin Portal"   
admin.site.index_title = "Welcome to KPI Notice Admin Panel"

