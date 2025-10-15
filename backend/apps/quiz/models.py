# quiz/models.py

from django.db import models
from apps.users.models import USER

class QuizQuestionGroup(models.Model):
    """题目组模型"""
    id = models.CharField(max_length=50, primary_key=True, verbose_name="组ID")
    title = models.CharField(max_length=200, verbose_name="组标题")
    description = models.TextField(verbose_name="组描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'quiz_question_group'
        verbose_name = '题目组'
        verbose_name_plural = '题目组'

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    """题目模型"""
    id = models.CharField(max_length=50, primary_key=True, verbose_name="题目ID")
    group = models.ForeignKey(
        QuizQuestionGroup,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="所属组"
    )
    text = models.TextField(verbose_name="题目内容")
    type = models.CharField(
        max_length=20,
        choices=[
            ('single', '单选题'),
            ('multiple', '多选题'),
            ('single-with-text', '单选带文本'),
            ('image-single', '图片单选'),
            ('image-multiple', '图片多选'),
            ('text', '文本题')
        ],
        verbose_name="题目类型"
    )
    image_range = models.JSONField(null=True, blank=True, verbose_name="图片范围")
    images_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="图片路径")
    min_selection = models.IntegerField(default=1, verbose_name="最小选择数")
    max_selection = models.IntegerField(default=1, verbose_name="最大选择数")
    show_text_when = models.CharField(max_length=255, null=True, blank=True, verbose_name="显示文本条件")
    sort_order = models.IntegerField(default=0, verbose_name="排序顺序")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'quiz_question'
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['sort_order']

    def __str__(self):
        return self.text[:50]

class QuizQuestionOption(models.Model):
    """题目选项模型"""
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name="所属题目"
    )
    label = models.CharField(max_length=500, verbose_name="选项文本")
    value = models.CharField(max_length=255, verbose_name="选项值")
    emoji = models.CharField(max_length=10, null=True, blank=True, verbose_name="表情符号")
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name="选项图片")
    sort_order = models.IntegerField(default=0, verbose_name="排序顺序")

    class Meta:
        db_table = 'quiz_question_option'
        verbose_name = '题目选项'
        verbose_name_plural = '题目选项'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.label} ({self.value})"

class UserQuizSession(models.Model):
    """用户测验会话模型"""
    STATUS_CHOICES = [
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('abandoned', '已放弃')
    ]
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='quiz_sessions',
        verbose_name="用户"
    )
    session_id = models.CharField(max_length=100, unique=True, verbose_name="会话ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="状态")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    duration_ms = models.IntegerField(null=True, blank=True, verbose_name="持续时间(毫秒)")
    current_part = models.IntegerField(default=1, verbose_name="当前所处阶段（1-4）")
    main_fragrance = models.CharField(max_length=50, default="", blank=True, verbose_name="主香调")
    secondary_fragrance = models.CharField(max_length=50, default="", blank=True, verbose_name="次香调")

    class Meta:
        db_table = 'user_quiz_session'
        verbose_name = '用户测验会话'
        verbose_name_plural = '用户测验会话'
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.username} - {self.session_id}"

class UserAnswer(models.Model):
    """用户答题记录模型"""
    session = models.ForeignKey(
        UserQuizSession,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="所属会话"
    )
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name="题目"
    )
    value = models.TextField(null=True, blank=True, verbose_name="答案值")
    text = models.TextField(null=True, blank=True, verbose_name="文本答案")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="答题时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'user_answer'
        verbose_name = '用户答题记录'
        verbose_name_plural = '用户答题记录'

    def __str__(self):
        return f"{self.session.session_id} - {self.question.id}"


class FragranceCategory(models.Model):
    """香调类别模型"""
    name = models.CharField(max_length=100, verbose_name="中文名称")
    english_name = models.CharField(max_length=100, verbose_name="英文名称")
    core_trait_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name="核心特质1(类型/强度)")
    core_trait_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="核心特质2(类型/强度)")
    intensity = models.CharField(max_length=20, null=True, blank=True, verbose_name="气味强度")
    style_keywords = models.TextField(null=True, blank=True, verbose_name="香气风格关键词")
    image_url = models.CharField(max_length=255, verbose_name="图片地址")
    category_type = models.CharField(max_length=50, verbose_name="香调类别")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = 'fragrance_category'
        verbose_name = '香调类别'
        verbose_name_plural = '香调类别'

    def __str__(self):
        return f"{self.name} ({self.english_name})"