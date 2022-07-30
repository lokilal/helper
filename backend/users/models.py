from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
        verbose_name='Профессия'
    )

    def __str__(self):
        return f'{self.profession.title} - {self.title}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING,
        verbose_name='Вопрос'
    )
    title = models.CharField(
        max_length=128, verbose_name='Ответ'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


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

    def __str__(self):
        return f'{self.user} - {self.question}'

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


class Feedback(models.Model):
    customer = models.ForeignKey(
        'Customer', on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    worker = models.ForeignKey(
        'Worker', on_delete=models.CASCADE,
        verbose_name='Работник'
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


class Profession(models.Model):
    title = models.CharField(
        max_length=64, verbose_name='Название профессии'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'


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
        default=0, verbose_name='Telegram ID'
    )
    gender = models.CharField(
        max_length=1, choices=GENDERS, default=MALE,
        verbose_name='Пол'
    )
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE,
        verbose_name='Профессия'
    )
    experience = models.DecimalField(
        max_digits=3, decimal_places=1,
        verbose_name='Опыт работы в годах',
        validators=[MinValueValidator(2)]
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2,
        verbose_name='Рейтинг', default=0
    )
    balance = models.PositiveBigIntegerField(
        verbose_name='Остаток на балансе', default=0
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['-created_at']


class Customer(models.Model):
    name = models.CharField(
        max_length=64, verbose_name='Контактные данные'
    )
    telegram_id = models.IntegerField(
        verbose_name='Telegram ID', default=0
    )
    free_period = models.BooleanField(
        default=False, verbose_name='Использован бесплатный период'
    )
    created_at = models.DateField(
        auto_now_add=True, verbose_name='Дата регистрации'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
