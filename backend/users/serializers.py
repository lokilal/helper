from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Schedule, Worker)


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        exclude = ('id', )


class WorkerSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    profession = ProfessionSerializer()

    class Meta:
        model = Worker
        exclude = ('id', 'balance', 'created_at', )


class WorkerCreateSerializer(serializers.ModelSerializer):
    profession = serializers.SlugRelatedField(
        queryset=Profession.objects.all(), slug_field='title'
    )

    class Meta:
        model = Worker
        exclude = ('created_at', )


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = ('id', 'created_at', )


class FeedbackSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field='telegram_id', queryset=Customer.objects.all()
    )
    worker = serializers.SlugRelatedField(
        slug_field='telegram_id', queryset=Worker.objects.all()
    )

    class Meta:
        model = Feedback
        exclude = ('id', )
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
