# quiz/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizQuestionGroupViewSet,
    UserQuizSessionViewSet,
    UserAnswerViewSet,
    get_all_questions,
    get_phased_questions,
    extend_text_with_ai
)

# 创建路由器
router = DefaultRouter()

# 注册题目组视图集
router.register(
    r'question-groups', 
    QuizQuestionGroupViewSet, 
    basename='question-group'
)

# 注册用户测验会话视图集
router.register(
    r'sessions', 
    UserQuizSessionViewSet, 
    basename='session'
)

# 为答题记录创建嵌套路由
# 答题记录需要与会话关联，所以使用嵌套路由
sessions_router = DefaultRouter()
sessions_router.register(
    r'answers', 
    UserAnswerViewSet, 
    basename='session-answers'
)

# 定义URL模式
urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
    
    # 嵌套路由：/sessions/{session_id}/answers/
    path('sessions/<str:session_id>/', include(sessions_router.urls)),
    
    # 获取所有题目（不分组）
    path('all-questions/', get_all_questions, name='get_all_questions'),
    
    # 分阶段获取问卷题目
    path('phased-questions/', get_phased_questions, name='phased-questions'),
    
    # AI扩写文本
    path('extend-text/', extend_text_with_ai, name='extend_text_with_ai'),
]