from django.contrib import admin

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Schedule, Worker, QuestionChoiceAnswer)


class QuestionChoiceAnswerInline(admin.StackedInline):
    model = QuestionChoiceAnswer
    extra = 0


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'profession', )
    list_filter = ('profession', )
    fieldsets = (
        ('Добавить вопрос', {'fields': ['title', 'profession']}),
    )
    inlines = [ChoiceInline]


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'question', 'created_at', )
    list_filter = ('question__profession', 'created_at')
    search_fields = ('customer', )
    inlines = [QuestionChoiceAnswerInline]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer', 'worker', 'score', 'created_at', )
    list_filter = ('created_at', )
    search_fields = ('customer', 'worker')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'profession', 'telegram_id', 'get_rating',
                    'balance', 'verified')
    list_filter = ('gender', 'profession', 'verified')
    search_fields = ('telegram_id', )
    list_editable = ('verified', )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'free_period', )
    list_filter = ('free_period', 'created_at', )
    search_fields = ('telegram_id', )


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('worker', 'customer', 'date', 'link', )
    list_filter = ('date', )
    search_fields = ('worker', 'customer', 'link', )


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profession)
