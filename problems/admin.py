from django.contrib import admin
from .models import Problem, ProblemStatus, Hint, Editorial

admin.site.register(Problem)
admin.site.register(ProblemStatus)
admin.site.register(Hint)
admin.site.register(Editorial)