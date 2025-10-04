# quiz/admin.py

from django.contrib import admin
from .models import (
    QuizQuestionGroup,
    QuizQuestion,
    QuizQuestionOption,
    UserQuizSession,
    UserAnswer
)

class QuizQuestionOptionInline(admin.TabularInline):
    """题目选项内联编辑"""
    model = QuizQuestionOption
    extra = 4  # 默认显示4个空选项
    fields = ('label', 'value', 'emoji', 'image', 'sort_order')

@admin.register(QuizQuestionGroup)
class QuizQuestionGroupAdmin(admin.ModelAdmin):
    """题目组管理"""
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'description')
    ordering = ('-created_at',)

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    """题目管理"""
    list_display = ('id', 'group', 'text', 'type', 'sort_order', 'created_at')
    list_filter = ('group', 'type')
    search_fields = ('id', 'text')
    ordering = ('group', 'sort_order')
    inlines = [QuizQuestionOptionInline]
    # 添加自定义的formfield_overrides来优化JSON字段的显示
    formfield_overrides = {
        # 这里可以添加自定义的JSON字段编辑器
    }

@admin.register(QuizQuestionOption)
class QuizQuestionOptionAdmin(admin.ModelAdmin):
    """题目选项管理"""
    list_display = ('id', 'question', 'label', 'value', 'sort_order')
    list_filter = ('question__group',)
    search_fields = ('label', 'value')
    ordering = ('question__group', 'question', 'sort_order')

@admin.register(UserQuizSession)
class UserQuizSessionAdmin(admin.ModelAdmin):
    """用户测验会话管理"""
    list_display = ('session_id', 'user', 'status', 'start_time', 'end_time', 'duration_ms')
    list_filter = ('status', 'start_time')
    search_fields = ('session_id', 'user__username')
    ordering = ('-start_time',)
    # 禁用编辑功能
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """用户答题记录管理"""
    list_display = ('id', 'session', 'question', 'created_at')
    list_filter = ('session__user', 'session__status')
    search_fields = ('session__session_id', 'question__text')
    ordering = ('-created_at',)
    # 禁用编辑功能
    def has_change_permission(self, request, obj=None):
        return False