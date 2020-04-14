from django.contrib import admin

# Register your models here.

from .models import Question, Session, Submission

admin.site.register(Question)
admin.site.register(Session)
admin.site.register(Submission)
