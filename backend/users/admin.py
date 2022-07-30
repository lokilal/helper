from django.contrib import admin

from .models import Question, QuestionAnswer, Profession, Worker, Customer, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Добавить вопрос', {'fields': ['title', 'question_type', 'profession']}),
    )
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer)
admin.site.register(Profession)
admin.site.register(Worker)
admin.site.register(Customer)
