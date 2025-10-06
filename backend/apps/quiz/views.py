# quiz/views.py

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .models import (
    QuizQuestionGroup,
    QuizQuestion,
    UserQuizSession,
    UserAnswer
)
from .serializers import (
    QuizQuestionGroupSerializer,
    QuizQuestionSerializer,
    UserQuizSessionSerializer,
    UserQuizSessionCreateSerializer,
    UserAnswerCreateSerializer,
    UserQuizSessionCompleteSerializer,
    UserQuizHistorySerializer
)
import json

class QuizQuestionGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """题目组视图集"""
    queryset = QuizQuestionGroup.objects.all()
    serializer_class = QuizQuestionGroupSerializer
    
    @action(detail=False, methods=['get'], url_path='all-questions')
    def all_questions(self, request):
        """获取所有题目组和题目"""
        # 获取所有题目组，并预加载相关题目和选项，优化查询性能
        groups = QuizQuestionGroup.objects.prefetch_related(
            'questions__options'
        ).order_by('id')
        
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='part/(?P<part>[0-9]+)')
    def get_part_questions(self, request, part=None):
        """获取特定部分的题目"""
        try:
            part = int(part)
            if part < 1 or part > 4:
                return Response(
                    {"code": 400, "msg": "部分参数无效，必须是1-4之间的整数"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取指定部分的题目组
            group_id = f"part{part}"
            try:
                group = QuizQuestionGroup.objects.get(id=group_id)
            except QuizQuestionGroup.DoesNotExist:
                return Response(
                    {"code": 404, "msg": f"第{part}部分题目组不存在"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 如果是Part4，需要根据用户会话动态生成选项
            if part == 4:
                # 获取用户会话ID
                session_id = request.query_params.get('session_id')
                if not session_id:
                    return Response(
                        {"code": 400, "msg": "Part4需要提供session_id参数"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    session = UserQuizSession.objects.get(session_id=session_id)
                except UserQuizSession.DoesNotExist:
                    return Response(
                        {"code": 404, "msg": "会话不存在"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # 生成动态Part4题目
                questions = self._generate_part4_questions(session)
                
                # 序列化题目数据
                serializer = QuizQuestionSerializer(questions, many=True)
                
                # 为动态生成的选项添加特殊处理
                for i, question_data in enumerate(serializer.data):
                    question = questions[i]
                    if hasattr(question, '_dynamic_options'):
                        # 序列化动态选项
                        dynamic_options = []
                        for option in question._dynamic_options:
                            option_data = {
                                'label': option.label,
                                'value': option.value,
                                'image': option.image
                            }
                            dynamic_options.append(option_data)
                        question_data['options'] = dynamic_options
                
                return Response({
                    "code": 200,
                    "msg": "获取成功",
                    "data": {
                        'part': part,
                        'title': group.title,
                        'description': group.description,
                        'questions': serializer.data
                    }
                })
            else:
                # 其他部分直接返回题目组数据
                serializer = QuizQuestionGroupSerializer(group)
                return Response({
                    "code": 200,
                    "msg": "获取成功",
                    "data": serializer.data
                })
        except ValueError:
            return Response(
                {"code": 400, "msg": "部分参数必须是整数"},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserQuizSessionViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """用户测验会话视图集"""
    queryset = UserQuizSession.objects.all()
    serializer_class = UserQuizSessionSerializer
    lookup_field = 'session_id'
    
    def get_queryset(self):
        """确保用户只能看到自己的会话"""
        user = self.request.user
        if user.is_superuser:
            return UserQuizSession.objects.all()
        return UserQuizSession.objects.filter(user=user)
    
    def destroy(self, request, *args, **kwargs):
        """删除测验会话（只能删除未完成的会话）"""
        instance = self.get_object()
        
        # 只允许删除未完成的会话
        if instance.status != 'in_progress':
            return Response(
                {'detail': '只能删除未完成的测验会话。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_serializer_class(self):
        """根据不同的操作返回不同的序列化器"""
        if self.action == 'create':
            return UserQuizSessionCreateSerializer
        elif self.action == 'complete':
            return UserQuizSessionCompleteSerializer
        elif self.action == 'history':
            return UserQuizHistorySerializer
        return self.serializer_class
    
    def create(self, request, *args, **kwargs):
        """创建新的测验会话"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 确保在创建会话时正确初始化current_part字段
        instance = serializer.save(current_part=1)
        
        # 获取创建后的会话数据
        session_serializer = UserQuizSessionSerializer(instance)
        return Response(
            session_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, session_id=None):
        """完成测验会话"""
        try:
            instance = self.get_object()
            if instance.status != 'in_progress':
                return Response(
                    {'detail': '该会话已经完成或已放弃，无法再次完成。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            
            return Response(
                UserQuizSessionSerializer(instance).data,
                status=status.HTTP_200_OK
            )
        except UserQuizSession.DoesNotExist:
            return Response(
                {'detail': '会话不存在。'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='check-incomplete')
    def check_incomplete_session(self, request):
        """检查用户是否有未完成的测验会话"""
        user = request.user
        
        # 查找最近的未完成会话
        incomplete_session = UserQuizSession.objects.filter(
            user=user,
            status='in_progress'
        ).order_by('-start_time').first()
        
        if incomplete_session:
            # 获取会话中的答案数量，用于显示进度
            answers_count = incomplete_session.answers.count()
            total_questions = QuizQuestion.objects.count()
            
            return Response({
                'has_incomplete': True,
                'session_id': incomplete_session.session_id,
                'start_time': incomplete_session.start_time,
                'answers_count': answers_count,
                'total_questions': total_questions
            })
        
        return Response({'has_incomplete': False})
        
    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        """获取用户的测验历史"""
        user = request.user
        # 默认获取最近10条记录，可以通过query参数调整
        limit = request.query_params.get('limit', 10)
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        
        # 获取所有会话（包括已完成和未完成的）
        sessions = UserQuizSession.objects.filter(
            user=user
        ).order_by('-start_time')[:limit]
        
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='submit-part/(?P<current_part>[0-9]+)')
    def submit_part(self, request, session_id=None, current_part=None):
        """提交当前阶段，进入下一阶段"""
        try:
            current_part = int(current_part)
            if current_part < 1 or current_part > 4:
                return Response(
                    {"code": 400, "msg": "部分参数无效，必须是1-4之间的整数"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            instance = self.get_object()
            if instance.status != 'in_progress':
                return Response(
                    {'detail': '该会话已结束，无法提交答案。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = SubmitPartSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {"code": 400, "msg": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            submitted_session_id = serializer.validated_data["session_id"]
            answers = serializer.validated_data["answers"]
            
            # 验证会话ID是否匹配
            if str(instance.session_id) != str(submitted_session_id):
                return Response(
                    {"code": 400, "msg": "会话ID不匹配"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 更新会话的当前部分
            instance.current_part = current_part + 1
            instance.save()
            
            # 保存答案
            for question_id, answer in answers.items():
                try:
                    question = QuizQuestion.objects.get(id=question_id)
                    # 将答案转为JSON字符串存储
                    if isinstance(answer, (list, dict)):
                        answer = json.dumps(answer)
                    
                    UserAnswer.objects.update_or_create(
                        session=instance,
                        question=question,
                        defaults={
                            'value': answer,
                            'part': current_part
                        }
                    )
                except QuizQuestion.DoesNotExist:
                    continue  # 跳过不存在的题目
            
            # 如果当前是Part3，生成Part4的题目
            if current_part == 3:
                part4_questions = self._generate_part4_questions(instance, answers)
                return Response({
                    "code": 200,
                    "msg": "Part3提交成功，已生成Part4题目",
                    "data": part4_questions
                })
            
            # 如果是Part4，标记会话为已完成
            if current_part == 4:
                instance.status = 'completed'
                instance.end_time = timezone.now()
                if instance.start_time:
                    duration = instance.end_time - instance.start_time
                    instance.duration_ms = int(duration.total_seconds() * 1000)
                instance.save()
                return Response({"code": 200, "msg": "问卷提交成功"})
            
            # 返回下一部分的题目
            next_part = current_part + 1
            group_id = f"part{next_part}"
            try:
                group = QuizQuestionGroup.objects.get(id=group_id)
                serializer = QuizQuestionGroupSerializer(group)
                return Response({
                    "code": 200,
                    "msg": f"Part{current_part}提交成功",
                    "data": serializer.data
                })
            except QuizQuestionGroup.DoesNotExist:
                return Response(
                    {"code": 404, "msg": f"第{next_part}部分题目组不存在"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except ValueError:
            return Response(
                {"code": 400, "msg": "部分参数必须是整数"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _generate_part4_questions(self, session):
        """
        根据用户前三个部分的回答生成个性化的Part4题目
        返回一个包含动态生成选项的题目列表
        """
        # 获取用户前三个部分的答案
        user_answers = UserAnswer.objects.filter(
            session=session,
            part__in=[1, 2, 3]
        )
        
        # 分析用户的香调偏好
        fragrance_profile = self._analyze_fragrance_profile(user_answers)
        
        # 获取Part4题目组
        try:
            part4_group = QuizQuestionGroup.objects.get(id='part4')
            questions = list(part4_group.questions.all())
            
            # 为每个题目动态生成选项
            for question in questions:
                if question.id == 'q4':  # 图片多选题
                    # 根据用户偏好生成香调组合选项
                    options = self._generate_fragrance_combinations(fragrance_profile)
                    
                    # 创建动态选项类
                    class DynamicOption:
                        def __init__(self, label, value, image):
                            self.label = label
                            self.value = value
                            self.image = image
                    
                    # 为q4添加动态生成的选项
                    question._dynamic_options = []
                    for option in options:
                        # 使用题目中配置的图片路径
                        image_path = f"{question.images_path}{option['value']}.png"
                        option_obj = DynamicOption(
                            label=option['label'],
                            value=option['value'],
                            image=image_path
                        )
                        question._dynamic_options.append(option_obj)
            
            return questions
        except QuizQuestionGroup.DoesNotExist:
            return []
    
    def _analyze_fragrance_profile(self, user_answers):
        """
        分析用户的香调偏好
        """
        profile = {
            'personality': {},  # 性格特点
            'sensitivity': {},   # 感官敏感度
            'relaxation': {},   # 放松场景
            'preferences': {}   # 香调偏好
        }
        
        for answer in user_answers:
            question_id = answer.question.id
            value = json.loads(answer.value) if answer.value else None
            
            if question_id.startswith('q1_'):  # Part1: 情景选择
                if question_id == 'q1_1':  # 性格特点
                    profile['personality'][value] = profile['personality'].get(value, 0) + 1
                elif question_id == 'q1_2':  # 放松场景
                    profile['relaxation'][value] = profile['relaxation'].get(value, 0) + 1
                    
            elif question_id.startswith('q2_'):  # Part2: 感官敏感度
                profile['sensitivity'][question_id] = value
                
            elif question_id.startswith('q3_'):  # Part3: 填空题
                # 分析填空题中的关键词
                if answer.text:
                    text = answer.text.lower()
                    if '花' in text or 'floral' in text:
                        profile['preferences']['floral'] = profile['preferences'].get('floral', 0) + 1
                    if '木' in text or 'woody' in text:
                        profile['preferences']['woody'] = profile['preferences'].get('woody', 0) + 1
                    if '柑' in text or 'citrus' in text:
                        profile['preferences']['citrus'] = profile['preferences'].get('citrus', 0) + 1
                    if '东' in text or 'oriental' in text:
                        profile['preferences']['oriental'] = profile['preferences'].get('oriental', 0) + 1
        
        return profile
    
    def _generate_fragrance_combinations(self, profile):
        """
        根据用户偏好生成香调组合选项
        """
        # 基础香调组合
        base_combinations = [
            {
                'label': '花香木质调',
                'value': 'floral_woody',
                'description': '优雅中带有温暖'
            },
            {
                'label': '柑橘海洋调',
                'value': 'citrus_aquatic',
                'description': '清新中带有自由'
            },
            {
                'label': '东方香料调',
                'value': 'oriental_spicy',
                'description': '神秘中带有热情'
            },
            {
                'label': '果香花调',
                'value': 'fruity_floral',
                'description': '活力中带有浪漫'
            },
            {
                'label': '木质烟草调',
                'value': 'woody_tobacco',
                'description': '沉稳中带有成熟'
            },
            {
                'label': '绿叶草本调',
                'value': 'green_herbal',
                'description': '自然中带有清新'
            },
            {
                'label': '皮革麝香调',
                'value': 'leather_musk',
                'description': '野性中带有温柔'
            },
            {
                'label': '香草美食调',
                'value': 'vanilla_gourmand',
                'description': '甜美中带有舒适'
            }
        ]
        
        # 根据用户偏好调整选项顺序
        preferences = profile.get('preferences', {})
        personality = profile.get('personality', {})
        
        # 根据性格特点调整权重
        if 'outgoing' in personality and personality['outgoing'] > 0:
            # 外向性格更喜欢明亮、活泼的香调
            for combo in base_combinations:
                if combo['value'] in ['citrus_aquatic', 'fruity_floral']:
                    combo['score'] = combo.get('score', 0) + 2
        
        if 'calm' in personality and personality['calm'] > 0:
            # 冷静性格更喜欢柔和、舒缓的香调
            for combo in base_combinations:
                if combo['value'] in ['floral_woody', 'green_herbal']:
                    combo['score'] = combo.get('score', 0) + 2
        
        # 根据香调偏好调整权重
        for pref, count in preferences.items():
            for combo in base_combinations:
                if pref in combo['value']:
                    combo['score'] = combo.get('score', 0) + count
        
        # 按分数排序并返回前5个选项
        sorted_combinations = sorted(
            base_combinations, 
            key=lambda x: x.get('score', 0), 
            reverse=True
        )
        
        return sorted_combinations[:5]  # 返回前5个最适合的选项
    
    @action(detail=True, methods=['get'], url_path='report')
    def report(self, request, session_id=None):
        """获取测验报告"""
        try:
            instance = self.get_object()
            # 检查会话是否已完成
            if instance.status != 'completed':
                return Response(
                    {'detail': '测验尚未完成，无法生成报告。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 构建报告数据
            report = {
                'session_id': instance.session_id,
                'start_time': instance.start_time.isoformat(),
                'end_time': instance.end_time.isoformat(),
                'duration_ms': instance.duration_ms,
                'time_spent': instance.duration_ms,  # 保持与前端期望的字段名一致
                'completed_at': instance.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_questions': instance.answers.count(),  # 添加题目数量
                'answers': {}
            }
            
            # 获取所有答案
            for answer in instance.answers.all():
                # 将value从JSON字符串转回原始数据类型
                try:
                    value = json.loads(answer.value) if answer.value else None
                except json.JSONDecodeError:
                    value = answer.value
                
                # 初始化选项文本
                option_label = None
                # 初始化选项标签列表（用于多选题）
                option_labels = []
                
                # 如果答案是对象并且有value字段（如{"value": "E"}）
                if isinstance(value, dict) and 'value' in value:
                    answer_value = value['value']
                    # 查找对应的选项文本
                    for option in answer.question.options.all():
                        if option.value == answer_value:
                            option_label = option.label
                            break
                # 如果答案是直接的字符串值
                elif isinstance(value, str):
                    for option in answer.question.options.all():
                        if option.value == value:
                            option_label = option.label
                            break
                # 如果答案是数组（多选题）
                elif isinstance(value, list):
                    for answer_item in value:
                        for option in answer.question.options.all():
                            if option.value == answer_item:
                                option_labels.append(option.label)
                                break
                
                report['answers'][answer.question.id] = {
                    'question_type': answer.question.type,  # 添加题目类型
                    'value': value,
                    'text': answer.text,
                    'question_text': answer.question.text,
                    'option_label': option_label,
                    'option_labels': option_labels,  # 用于多选题的所有选项标签
                }
            
            return Response(report)
        except UserQuizSession.DoesNotExist:
            return Response(
                {'detail': '会话不存在。'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='submit-first-20')
    def submit_first_20(self, request, session_id=None):
        """提交前20题答案并获取香调偏好"""
        try:
            instance = self.get_object()
            # 检查会话是否在进行中
            if instance.status != 'in_progress':
                return Response(
                    {'detail': '该会话已结束，无法提交答案。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取提交的前20题答案
            answers = request.data.get('answers', {})
            
            # 这里应该实现根据答案分析用户香调偏好的逻辑
            # 由于这是示例实现，我们返回一些模拟的香调图片数据
            fragrance_images = [
                {
                    'id': 'floral',
                    'name': '花香调',
                    'image_url': '/images/smell/花卉类（除白色花卉）/三叶草.png'
                },
                {
                    'id': 'white_floral',
                    'name': '白色花香调',
                    'image_url': '/images/smell/白色花卉/亚马逊月光花.png'
                },
                {
                    'id': 'woody',
                    'name': '木质调',
                    'image_url': '/images/smell/树木、苔藓/云杉.png'
                },
                {
                    'id': 'citrus',
                    'name': '柑橘调',
                    'image_url': '/images/smell/柑橘类/克里曼丁红橘.png'
                },
                {
                    'id': 'spicy',
                    'name': '辛辣调',
                    'image_url': '/images/smell/辛香料/八角.png'
                },
                {
                    'id': 'green',
                    'name': '草本绿叶调',
                    'image_url': '/images/smell/草本、绿叶/不凋花.png'
                }
            ]
            
            # 返回香调图片数据
            return Response({
                'fragrance_images': fragrance_images
            })
        except UserQuizSession.DoesNotExist:
            return Response(
                {'detail': '会话不存在。'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserAnswerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """用户答题记录视图集"""
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerCreateSerializer
    
    def create(self, request, *args, **kwargs):
        """保存或更新用户答案"""
        # 从URL中获取session_id
        session_id = kwargs.get('session_id')
        if not session_id:
            return Response(
                {'detail': '会话ID不能为空。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 检查会话是否存在且属于当前用户
            session = UserQuizSession.objects.get(
                session_id=session_id,
                user=request.user
            )
            
            # 检查会话状态
            if session.status != 'in_progress':
                return Response(
                    {'detail': '该会话已结束，无法保存答案。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 处理单个答案
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # 将session_id传入serializer的context
            serializer.context['session_id'] = session_id
            
            instance = serializer.save()
            
            # 返回成功响应
            return Response(
                {'detail': '答案保存成功。'},
                status=status.HTTP_201_CREATED
            )
        except UserQuizSession.DoesNotExist:
            return Response(
                {'detail': '会话不存在或不属于当前用户。'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phased_questions(request):
    """
    分阶段获取问卷题目
    参数：
    - part: 题目部分 (1-4)
    - session_id: 会话ID (Part4必需)
    """
    part = request.query_params.get('part')
    session_id = request.query_params.get('session_id')
    
    # 验证part参数
    if not part or not part.isdigit() or int(part) < 1 or int(part) > 4:
        return Response(
            {"code": 400, "msg": "部分参数必须是1-4之间的整数"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    part = int(part)
    
    try:
        # 获取指定部分的题目组
        group = QuizQuestionGroup.objects.get(id=f'part{part}')
        
        # 如果是Part4，需要根据用户会话动态生成选项
        if part == 4:
            if not session_id:
                return Response(
                    {"code": 400, "msg": "Part4需要提供session_id参数"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                session = UserQuizSession.objects.get(session_id=session_id)
            except UserQuizSession.DoesNotExist:
                return Response(
                    {"code": 404, "msg": "会话不存在"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 获取UserQuizSessionViewSet实例来调用_generate_part4_questions方法
            viewset = UserQuizSessionViewSet()
            viewset.request = request
            
            # 生成动态Part4题目
            questions = viewset._generate_part4_questions(session)
            
            # 序列化题目数据
            serializer = QuizQuestionSerializer(questions, many=True)
            
            # 构建返回数据，与其他部分格式保持一致
            return_data = {
                'id': group.id,
                'title': group.title,
                'description': group.description,
                'questions': serializer.data
            }
            
            return Response({
                "code": 200,
                "msg": "获取成功",
                "data": return_data
            })
        else:
            # 其他部分直接返回题目组数据
            serializer = QuizQuestionGroupSerializer(group)
            return Response({
                "code": 200,
                "msg": "获取成功",
                "data": serializer.data
            })
            
    except QuizQuestionGroup.DoesNotExist:
        return Response(
            {"code": 404, "msg": f"第{part}部分题目组不存在"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def get_all_questions(request):
    """获取所有题目（不分组）"""
    questions = QuizQuestion.objects.prefetch_related('options').order_by('id')
    serializer = QuizQuestionSerializer(questions, many=True)
    return Response(serializer.data)

# 用于AI扩写文本的视图
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extend_text_with_ai(request):
    """使用AI扩写用户输入的文本"""
    try:
        # 获取用户输入的文本
        text = request.data.get('text', '')
        if not text.strip():
            return Response(
                {'detail': '文本不能为空。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 导入必要的库
        from openai import OpenAI
        from django.conf import settings
        
        # 从settings中获取阿里云百炼API密钥
        dashscope_api_key = getattr(settings, 'DASHSCOPE_API_KEY', '')
        if not dashscope_api_key:
            return Response(
                {'detail': '阿里云百炼API密钥未配置。'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 创建OpenAI客户端，连接到阿里云百炼API
        client = OpenAI(
            api_key=dashscope_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        # 调用AI模型扩写文本
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的文案扩写助手，擅长将简洁的描述扩展为更丰富、生动的表达。请保持原文的核心意思，同时增加细节和表现力。尽可能详细的描述用户感觉最舒适的场景，字数控制在30字以内"},
                {"role": "user", "content": f"请扩写以下文本：{text}"},
            ],
            # 对于qwen-plus模型，不需要设置enable_thinking
        )
        
        # 提取扩写后的文本
        extended_text = completion.choices[0].message.content
        
        # 返回扩写结果
        return Response({
            'extended_text': extended_text
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        # 记录错误日志
        print(f"AI扩写失败: {str(e)}")
        return Response(
            {'detail': f'AI扩写失败，请稍后重试。错误信息：{str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )