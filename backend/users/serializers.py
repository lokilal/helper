from rest_framework import serializers

from .models import (Choice, Customer, Feedback, Profession, Question,
                     QuestionAnswer, Worker, Schedule)


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


