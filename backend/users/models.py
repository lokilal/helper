from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Schedule(models.Model):
    worker = models.ForeignKey(
        'Worker', on_delete=models.DO_NOTHING,
        related_name='schedules',
        verbose_name='Работник'
    )
    customer = models.ForeignKey(
        'Customer', on_delete=models.DO_NOTHING,
        related_name='schedules',
        verbose_name='Пользователь'
    )
    date = models.DateTimeField(
        verbose_name='Время встречи', db_index=True
    )
    link = models.URLField(
        verbose_name='Ссылка на комнату'
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-date']


class Question(models.Model):
    QUESTION_TYPE = [
        ('checkbox', 'Несколько вариантов'),
        ('text', 'Текст'),
    ]
    title = models.CharField(
        max_length=128, verbose_name='Вопрос'
    )
    question_type = models.CharField(
        choices=QUESTION_TYPE, default='checkbox',
        max_length=8, verbose_name='Вид ответа'
    )
    profession = models.ForeignKey(
        'Profession', on_delete=models.CASCADE,
        verbose_name='Профессия', related_name='questions'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.profession.title} - {self.title}'


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING,
        verbose_name='Вопрос', related_name='choices'
    )
    title = models.CharField(
        max_length=128, verbose_name='Ответ'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.title}'


class QuestionAnswer(models.Model):
    user = models.IntegerField(
        default=0, verbose_name='Telegram ID',
        db_index=True
    )
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING,
        verbose_name='Вопрос'
    )
    choice = models.ForeignKey(
        Choice, on_delete=models.DO_NOTHING,
        verbose_name='Ответ', blank=True, null=True
    )
    answer_text = models.TextField(
        blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата ответа'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'choice'],
                name='unique_user_choice'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.question}'


class Feedback(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='feedbacks'
    )
    worker = models.ForeignKey(
        'Worker', on_delete=models.CASCADE,
        verbose_name='Работник', related_name='feedbacks'
    )
    comment = models.TextField(
        max_length=512, verbose_name='Комментарий'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка', null=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'worker'],
                name='unique_customer_worker'
            )
        ]

    def __str__(self):
        return f'{self.customer} - {self.worker}'


class Profession(models.Model):
    title = models.CharField(
        max_length=64, verbose_name='Название профессии'
    )

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

    def __str__(self):
        return self.title


class Worker(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
    ]
    name = models.CharField(
        max_length=64, verbose_name='Имя рабочего'
    )
    telegram_id = models.IntegerField(
        verbose_name='Telegram ID', unique=True
    )
    gender = models.CharField(
        max_length=1, choices=GENDERS, default=MALE,
        verbose_name='Пол'
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE,
        verbose_name='Профессия', related_name='workers'
    )
    experience = models.DecimalField(
        max_digits=3, decimal_places=1,
        verbose_name='Опыт работы в годах',
        validators=[MinValueValidator(2)]
    )
    balance = models.PositiveBigIntegerField(
        verbose_name='Остаток на балансе', default=0
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def get_rating(self):
        return Feedback.objects.filter(
            worker__telegram_id=self.telegram_id
        ).aggregate(models.Avg('score'))['score__avg']

    get_rating.fget.short_description = 'Рейтинг'


class Customer(models.Model):
    name = models.CharField(
        max_length=64, verbose_name='Контактные данные'
    )
    telegram_id = models.IntegerField(
        verbose_name='Telegram ID', unique=True
    )
    free_period = models.BooleanField(
        default=False, verbose_name='Использован бесплатный звонок'
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата регистрации'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
