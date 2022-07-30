from django.contrib import admin

from .models import Question, QuestionAnswer, Profession, Worker, Customer, Choice, Feedback


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'profession', 'question_type', )
    list_filter = ('profession', )
    fieldsets = (
        ('Добавить вопрос', {'fields': ['title', 'question_type', 'profession']}),
    )
    inlines = [ChoiceInline]


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at', )
    list_filter = ('question', 'created_at')
    search_fields = ('user', )


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer', 'worker', 'score', 'created_at', )
    list_filter = ('created_at', )
    search_fields = ('customer', 'worker')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'profession', 'telegram_id', 'rating', 'balance', )
    list_filter = ('gender', 'profession')
    search_fields = ('telegram_id', )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id', 'free_period', )
    list_filter = ('free_period', 'created_at', )
    search_fields = ('telegram_id', )


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profession)
