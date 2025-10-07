from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'question-groups', views.QuizQuestionGroupViewSet)
router.register(r'sessions', views.UserQuizSessionViewSet)

# 应用命名空间
app_name = 'quiz'

urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
    
    # 嵌套路由：会话下的答案
    path('sessions/<str:session_id>/answers/', views.UserAnswerViewSet.as_view({'post': 'create'}), name='user-answer-create'),
    
    # 自定义URL模式
    path('all-questions/', views.get_all_questions, name='all-questions'),
    path('phased-questions/', views.get_phased_questions, name='phased-questions'),
    path('extend-text/', views.extend_text_with_ai, name='extend-text'),
    path('fragrance-images/', views.get_fragrance_images, name='fragrance-images'),
]