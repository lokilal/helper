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
    class Meta:
        model = Customer
        exclude = ('id', 'created_at',)


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

    class Meta:
        model = Question
        exclude = ('id', 'profession',)

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

    class Meta:
        model = QuestionAnswer
        exclude = ('id',)

    def validate(self, attrs):
        choice = self.initial_data.get('choice')
        answer_text = attrs.get('answer_text')
        if not choice and not answer_text:
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
        if all(['choice', 'answer_text']) in self.initial_data:
            raise ValidationError(
                'answer_text и choice присутствуют в одном запросе'
            )
        if 'choice' in self.initial_data:
            choices = self.initial_data.pop('choice')
            for choice in choices:
                obj = get_object_or_404(Choice, title=choice['title'])
                QuestionChoiceAnswer.objects.create(
                    question_answer=instance, choice=obj
                )
        else:
            instance.answer_text = validated_data.get('answer_text', instance.answer_text)
            instance.save()
        return instance
