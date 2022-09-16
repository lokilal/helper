from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pytils.translit import slugify

from .validators import schedule_time_validator


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
        verbose_name='Время встречи', db_index=True,
        validators=[schedule_time_validator]
    )
    link = models.URLField(
        verbose_name='Ссылка на комнату',
        null=True
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-date']

    def save(self, *args, **kwargs):
        self.link = 'https://vk.com/'
        return super(Schedule, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.worker} - {self.customer}: {self.date}'


class Question(models.Model):
    title = models.CharField(
        max_length=128, verbose_name='Вопрос'
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


class QuestionChoiceAnswer(models.Model):
    question_answer = models.ForeignKey(
        'QuestionAnswer', on_delete=models.CASCADE,
        verbose_name='Ответ пользователя'
    )
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE,
        verbose_name='Ответ пользователя'
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'
        constraints = [
            models.UniqueConstraint(fields=['question_answer', 'choice'],
                                    name='unique_question_answer_choice')
        ]

    def __str__(self):
        return str(self.question_answer.customer)


class QuestionAnswer(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='answers'
    )
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING,
        verbose_name='Вопрос',
    )
    choice = models.ManyToManyField(
        Choice, through='QuestionChoiceAnswer',
        verbose_name='Ответ', blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата ответа'
    )

    class Meta:
        ordering = ['customer__telegram_id']
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    def __str__(self):
        return f'{self.customer} - {self.question}'


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
    slug = models.SlugField(
        blank=True, null=True,
        unique=True
    )

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Profession, self).save(*args, **kwargs)


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
        verbose_name='Telegram ID', unique=True, db_index=True
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
    about = models.TextField(
        verbose_name='Краткое описание'
    )
    balance = models.PositiveBigIntegerField(
        verbose_name='Остаток на балансе', default=0
    )
    verified = models.BooleanField(
        default=False, verbose_name='Проверенный'
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
        worker = Worker.objects.get(telegram_id=self.telegram_id)
        return worker.feedbacks.all().aggregate(models.Avg('score'))['score__avg']
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
