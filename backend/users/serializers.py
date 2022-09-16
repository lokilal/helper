from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from django.shortcuts import get_object_or_404

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Schedule, Worker, QuestionChoiceAnswer)


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        exclude = ('id',)


class WorkerSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    profession = ProfessionSerializer()

    class Meta:
        model = Worker
        exclude = ('id', 'balance', 'created_at',)


class WorkerCreateSerializer(serializers.ModelSerializer):
    profession = serializers.SlugRelatedField(
        queryset=Profession.objects.all(), slug_field='title'
    )

    class Meta:
        model = Worker
        exclude = ('created_at',)


class CustomerSerializer(serializers.ModelSerializer):
    questionnaires = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        exclude = ('id', 'created_at',)

    def get_questionnaires(self, obj):
        queryset = QuestionAnswer.objects.filter(customer=obj)
        questionnaires_profession_name = set()
        for answer in queryset:
            questionnaires_profession_name.add(answer.question.profession.title)
        return list(questionnaires_profession_name)


class FeedbackSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field='telegram_id', queryset=Customer.objects.all()
    )
    worker = serializers.SlugRelatedField(
        slug_field='telegram_id', queryset=Worker.objects.all()
    )

    class Meta:
        model = Feedback
        exclude = ('id',)
        validators = (
            UniqueTogetherValidator(
                queryset=Feedback.objects.all(), fields=('customer', 'worker'),
                message='Вы уже оставили отзыв'
            ),
        )

    def validate(self, attrs):
        if attrs['customer'] == attrs['worker']:
            raise ValidationError('Нельзя поставить отзыв самому себе')
        return attrs


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ('id', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField(read_only=True)
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = Question
        exclude = ('id',)

    def get_choices(self, obj):
        choices = obj.choices.all()
        return ChoiceSerializer(choices, many=True).data


class QuestionAnswerSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field='telegram_id', queryset=Customer.objects.all()
    )
    question = serializers.SlugRelatedField(
        slug_field='title', queryset=Question.objects.all()
    )
    profession = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionAnswer
        exclude = ('id',)

    def get_profession(self, obj):
        return obj.question.profession.title

    def validate(self, attrs):
        choice = self.initial_data.get('choice')
        answer_text = attrs.get('answer_text')
        if not choice :
            raise ValidationError(
                'Не представлено ответа'
            )
        return attrs

    def create(self, validated_data):
        question_answer = QuestionAnswer.objects.create(**validated_data)
        if 'choice' in self.initial_data:
            choices = self.initial_data.pop('choice')
            for choice in choices:
                obj = get_object_or_404(Choice, title=choice['title'])
                QuestionChoiceAnswer.objects.create(
                    question_answer=question_answer, choice=obj
                )
        return question_answer

    def update(self, instance, validated_data):
        instance.choice.clear()
        if 'choice' in self.initial_data:
            choices = self.initial_data.pop('choice')
            for choice in choices:
                obj = get_object_or_404(Choice, title=choice['title'])
                QuestionChoiceAnswer.objects.create(
                    question_answer=instance, choice=obj
                )
        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    class Meta:
        model = Schedule
        exclude = ('id', )
