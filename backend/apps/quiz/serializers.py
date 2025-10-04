# quiz/serializers.py

from rest_framework import serializers
from .models import (
    QuizQuestionGroup,
    QuizQuestion,
    QuizQuestionOption,
    UserQuizSession,
    UserAnswer
)
from apps.users.models import USER
import json

class QuizQuestionOptionSerializer(serializers.ModelSerializer):
    """题目选项序列化器"""
    class Meta:
        model = QuizQuestionOption
        fields = ['label', 'value', 'emoji', 'image']

class QuizQuestionSerializer(serializers.ModelSerializer):
    """题目序列化器"""
    options = QuizQuestionOptionSerializer(many=True, read_only=True)
    group_id = serializers.CharField(source='group.id', read_only=True)
    group_title = serializers.CharField(source='group.title', read_only=True)
    group_description = serializers.CharField(source='group.description', read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'group_id', 'group_title', 'group_description', 'text', 'type',
            'image_range', 'images_path', 'min_selection', 'max_selection',
            'show_text_when', 'options'
        ]

class QuizQuestionGroupSerializer(serializers.ModelSerializer):
    """题目组序列化器"""
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestionGroup
        fields = ['id', 'title', 'description', 'questions']

class UserAnswerSerializer(serializers.ModelSerializer):
    """用户答题记录序列化器"""
    question_id = serializers.CharField(source='question.id', read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['question_id', 'value', 'text', 'created_at']

class UserQuizSessionSerializer(serializers.ModelSerializer):
    """用户测验会话序列化器"""
    user = serializers.CharField(source='user.username', read_only=True)
    answers = UserAnswerSerializer(many=True, read_only=True)
    completed_at = serializers.DateTimeField(source='end_time', read_only=True)
    time_spent = serializers.IntegerField(source='duration_ms', read_only=True)
    total_questions = serializers.SerializerMethodField(read_only=True)
    
    def get_total_questions(self, obj):
        return obj.answers.count()

    class Meta:
        model = UserQuizSession
        fields = [
            'session_id', 'status', 'start_time', 'end_time', 
            'duration_ms', 'user', 'answers', 'completed_at', 
            'time_spent', 'total_questions'
        ]

class UserQuizSessionCreateSerializer(serializers.Serializer):
    """创建用户测验会话序列化器"""
    def create(self, validated_data):
        from django.utils.crypto import get_random_string
        user = self.context['request'].user
        session_id = f"AROMA_{get_random_string(32)}"
        return UserQuizSession.objects.create(
            user=user,
            session_id=session_id
        )

class UserAnswerCreateSerializer(serializers.Serializer):
    """创建用户答题记录序列化器"""
    question_id = serializers.CharField(required=True)
    value = serializers.JSONField(required=False, allow_null=True)
    text = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_question_id(self, value):
        try:
            QuizQuestion.objects.get(id=value)
            return value
        except QuizQuestion.DoesNotExist:
            raise serializers.ValidationError("题目不存在")

    def create(self, validated_data):
        session_id = self.context['session_id']
        question_id = validated_data['question_id']
        value = validated_data.get('value')
        text = validated_data.get('text')
        
        try:
            session = UserQuizSession.objects.get(session_id=session_id)
            question = QuizQuestion.objects.get(id=question_id)
            
            # 将value转为JSON字符串存储
            value_str = json.dumps(value) if value is not None else None
            
            # 检查是否已有该题的答案，如果有则更新
            user_answer, created = UserAnswer.objects.update_or_create(
                session=session,
                question=question,
                defaults={'value': value_str, 'text': text}
            )
            
            return user_answer
        except UserQuizSession.DoesNotExist:
            raise serializers.ValidationError("会话不存在")

class UserQuizSessionCompleteSerializer(serializers.Serializer):
    """完成用户测验会话序列化器"""
    def update(self, instance, validated_data):
        from django.utils import timezone
        instance.status = 'completed'
        instance.end_time = timezone.now()
        instance.duration_ms = int((instance.end_time - instance.start_time).total_seconds() * 1000)
        instance.save()
        return instance

class UserQuizHistorySerializer(serializers.ModelSerializer):
    """用户测验历史记录序列化器"""
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = UserQuizSession
        fields = [
            'session_id', 'status', 'start_time', 'end_time', 
            'duration_ms', 'answer_count'
        ]
        read_only_fields = fields
    
    def get_answer_count(self, obj):
        return obj.answers.count()