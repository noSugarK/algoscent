# quiz/views.py

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.crypto import get_random_string

from backend import settings
from .models import (
    QuizQuestionGroup,
    QuizQuestion,
    QuizQuestionOption,
    UserQuizSession,
    UserAnswer,
    FragranceCategory
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
    
    @action(detail=True, methods=['post'], url_path='submit-first-20')
    def submit_first_20(self, request, session_id=None):
        """提交前20道题的答案"""
        try:
            instance = self.get_object()
            if instance.status != 'in_progress':
                return Response(
                    {'detail': '该会话已结束，无法提交答案。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取提交的答案
            answers = request.data.get('answers', {})
            if not answers:
                return Response(
                    {'detail': '答案不能为空。'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
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
                            'part': 1  # 前20道题属于第一部分
                        }
                    )
                except QuizQuestion.DoesNotExist:
                    continue  # 跳过不存在的题目
            
            # 分析用户答案，确定主香调和次香调
            fragrance_analysis = self._analyze_user_answers_for_fragrance(instance)
            
            # 更新会话状态，标记为已完成第一部分
            instance.current_part = 2
            instance.main_fragrance = fragrance_analysis.get('main_fragrance')
            instance.secondary_fragrance = fragrance_analysis.get('secondary_fragrance')
            instance.save()
            
            return Response({
                'detail': '前20道题答案提交成功。',
                'session_id': instance.session_id,
                'current_part': instance.current_part,
                'main_fragrance': instance.main_fragrance,
                'secondary_fragrance': instance.secondary_fragrance
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'detail': f'提交答案失败：{str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='report')
    def report(self, request, session_id=None):
        """
        获取测验报告
        """
        try:
            session = self.get_object()
            
            # 检查会话是否已完成
            if session.status != 'completed':
                return Response(
                    {"code": 400, "msg": "测验尚未完成，无法生成报告"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 获取用户答案
            user_answers = UserAnswer.objects.filter(session=session).select_related('question').order_by('question__sort_order')
            
            # 构建答案数据
            answers_data = {}
            for answer in user_answers:
                # 获取问题信息
                question = answer.question
                question_text = question.text
                question_type = question.type
                
                # 获取选项信息（如果是选择题）
                option_labels = []
                option_label = None
                
                if question_type in ['single', 'multiple', 'single-with-text']:
                    try:
                        # 处理答案值
                        answer_value = answer.value
                        if isinstance(answer_value, str):
                            try:
                                # 尝试解析JSON字符串
                                parsed_value = json.loads(answer_value)
                                answer_value = parsed_value
                            except json.JSONDecodeError:
                                # 如果不是JSON字符串，保持原值
                                pass
                        
                        # 根据问题类型处理答案
                        if question_type == 'multiple' and isinstance(answer_value, list):
                            # 多选题
                            for option_value in answer_value:
                                try:
                                    # 根据选项值获取选项标签
                                    option = QuizQuestionOption.objects.get(
                                        question=question,
                                        value=option_value
                                    )
                                    option_labels.append(option.label)
                                except QuizQuestionOption.DoesNotExist:
                                    # 如果找不到选项，使用选项值作为标签
                                    option_labels.append(f"选项 {option_value}")
                        elif question_type in ['single', 'single-with-text'] and isinstance(answer_value, (str, int, dict)):
                            # 单选题或单选填空题
                            option_value = None
                            text_value = None
                            
                            if isinstance(answer_value, dict):
                                option_value = answer_value.get('value')
                                text_value = answer_value.get('text')
                            else:
                                option_value = answer_value
                            
                            if option_value:
                                try:
                                    # 根据选项值获取选项标签
                                    option = QuizQuestionOption.objects.get(
                                        question=question,
                                        value=option_value
                                    )
                                    option_label = option.label
                                except QuizQuestionOption.DoesNotExist:
                                    # 如果找不到选项，使用选项值作为标签
                                    option_label = f"选项 {option_value}"
                    except Exception as e:
                        print(f"处理选项信息时出错: {str(e)}")
                
                # 构建答案数据
                answer_data = {
                    'question_id': question.id,
                    'question_text': question_text,
                    'question_type': question_type,
                    'value': answer.value,
                    'option_label': option_label,
                    'option_labels': option_labels if option_labels else None,
                    'text': answer.text
                }
                
                answers_data[question.id] = answer_data
            
            # 计算测验用时
            time_spent = session.duration_ms  # 直接使用模型中存储的持续时间
            
            # 构建报告数据
            report_data = {
                'session_id': session.session_id,
                'started_at': session.start_time.isoformat() if session.start_time else None,
                'completed_at': session.end_time.isoformat() if session.end_time else None,
                'time_spent': time_spent,
                'total_questions': user_answers.count(),
                'main_fragrance': session.main_fragrance,
                'secondary_fragrance': session.secondary_fragrance,
                'answers': answers_data
            }
            
            return Response({
                "code": 200,
                "msg": "获取报告成功",
                "data": report_data
            })
            
        except Exception as e:
            print(f"获取测验报告失败: {str(e)}")
            return Response(
                {"code": 500, "msg": f"获取报告失败: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _analyze_user_answers_for_fragrance(self, session):
        """
        分析用户答案，确定主香调和次香调
        """
        # 获取用户的所有答案
        user_answers = UserAnswer.objects.filter(session=session, part=1)
        
        # 初始化香调计数器
        fragrance_counts = {
            '柑橘类': 0,
            '花卉类': 0,
            '木质类': 0,
            '东方类': 0,
            '西普类': 0,
            '皮革类': 0,
            '馥奇类': 0,
            '绿叶类': 0,
            '水生类': 0,
            '美食类': 0,
            '蔬果类': 0,
            '其他': 0
        }
        
        # 根据用户答案增加相应香调的计数
        for answer in user_answers:
            try:
                # 解析答案值
                answer_value = answer.value
                if isinstance(answer_value, str):
                    try:
                        # 尝试解析JSON
                        parsed_value = json.loads(answer_value)
                        if isinstance(parsed_value, (list, dict)):
                            answer_value = parsed_value
                    except json.JSONDecodeError:
                        # 不是JSON，保持原值
                        pass
                
                # 根据题目ID和答案值增加香调计数
                question_id = answer.question.id
                if question_id.startswith('q1'):
                    # 第一部分题目，根据答案值确定香调偏好
                    if isinstance(answer_value, list):
                        # 多选题
                        for value in answer_value:
                            self._update_fragrance_count(fragrance_counts, value)
                    else:
                        # 单选题
                        self._update_fragrance_count(fragrance_counts, answer_value)
                elif question_id.startswith('q2'):
                    # 第二部分题目，根据答案值确定香调偏好
                    if isinstance(answer_value, list):
                        # 多选题
                        for value in answer_value:
                            self._update_fragrance_count(fragrance_counts, value)
                    else:
                        # 单选题
                        self._update_fragrance_count(fragrance_counts, answer_value)
                elif question_id.startswith('q3'):
                    # 第三部分题目，根据答案值确定香调偏好
                    if isinstance(answer_value, list):
                        # 多选题
                        for value in answer_value:
                            self._update_fragrance_count(fragrance_counts, value)
                    else:
                        # 单选题
                        self._update_fragrance_count(fragrance_counts, answer_value)
            except Exception as e:
                print(f"处理答案时出错: {e}")
                continue
        
        # 找出计数最高的两个香调
        sorted_fragrances = sorted(fragrance_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 确保至少有两个香调
        if len(sorted_fragrances) >= 2:
            main_fragrance = sorted_fragrances[0][0]
            secondary_fragrance = sorted_fragrances[1][0]
        elif len(sorted_fragrances) == 1:
            main_fragrance = sorted_fragrances[0][0]
            secondary_fragrance = '花卉类'  # 默认次香调
        else:
            main_fragrance = '柑橘类'  # 默认主香调
            secondary_fragrance = '花卉类'  # 默认次香调
        
        return {
            'main_fragrance': main_fragrance,
            'secondary_fragrance': secondary_fragrance
        }

    def _update_fragrance_count(self, fragrance_counts, answer_value):
        """
        根据答案值更新香调计数
        """
        # 将答案值转换为字符串
        answer_str = str(answer_value).lower()
        
        # 根据答案值的关键词增加相应香调的计数
        if '柑橘' in answer_str or '柠檬' in answer_str or '橙' in answer_str or '柚' in answer_str:
            fragrance_counts['柑橘类'] += 1
        elif '花' in answer_str or '玫瑰' in answer_str or '茉莉' in answer_str or '薰衣草' in answer_str:
            fragrance_counts['花卉类'] += 1
        elif '木' in answer_str or '檀香' in answer_str or '雪松' in answer_str or '橡木' in answer_str:
            fragrance_counts['木质类'] += 1
        elif '东' in answer_str or '香料' in answer_str or '麝香' in answer_str or '香草' in answer_str:
            fragrance_counts['东方类'] += 1
        elif '西普' in answer_str or '苔藓' in answer_str or '橡树' in answer_str:
            fragrance_counts['西普类'] += 1
        elif '皮' in answer_str or '烟草' in answer_str or '烟' in answer_str:
            fragrance_counts['皮革类'] += 1
        elif '馥奇' in answer_str or '草' in answer_str or '树' in answer_str:
            fragrance_counts['馥奇类'] += 1
        elif '绿' in answer_str or '叶' in answer_str or '茶' in answer_str:
            fragrance_counts['绿叶类'] += 1
        elif '水' in answer_str or '海' in answer_str or '雨' in answer_str:
            fragrance_counts['水生类'] += 1
        elif '食' in answer_str or '甜' in answer_str or '巧' in answer_str or '奶' in answer_str:
            fragrance_counts['美食类'] += 1
        elif '果' in answer_str or '蔬' in answer_str or '苹果' in answer_str or '梨' in answer_str:
            fragrance_counts['蔬果类'] += 1
        else:
            fragrance_counts['其他'] += 1

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
                part4_questions = self._generate_part4_questions(instance)
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
        
        # 调用AI接口获取主香调和次香调
        fragrance_result = self._generate_fragrance_combinations()
        
        # 保存香调结果到会话中，以便下次使用
        session.main_fragrance = fragrance_result['main_fragrance']
        session.secondary_fragrance = fragrance_result['secondary_fragrance']
        # print(fragrance_result)
        session.save()
        
        # 获取Part4题目组
        try:
            part4_group = QuizQuestionGroup.objects.get(id='part4')
            questions = list(part4_group.questions.all())
            
            # 为每个题目动态生成选项
            for question in questions:
                if question.id == 'q4':  # 图片多选题
                    # 创建动态选项类
                    class DynamicOption:
                        def __init__(self, label, value, image):
                            self.label = label
                            self.value = value
                            self.image = image
                    
                    # 为q4添加动态生成的选项
                    question._dynamic_options = []
                    
                    # 添加主香调选项
                    main_option = DynamicOption(
                        label=fragrance_result['main_fragrance'],
                        value=fragrance_result['main_fragrance'],
                        image=f"{question.images_path}{fragrance_result['main_fragrance']}.png"
                    )
                    question._dynamic_options.append(main_option)
                    
                    # 添加次香调选项
                    secondary_option = DynamicOption(
                        label=fragrance_result['secondary_fragrance'],
                        value=fragrance_result['secondary_fragrance'],
                        image=f"{question.images_path}{fragrance_result['secondary_fragrance']}.png"
                    )
                    question._dynamic_options.append(secondary_option)
            
            return questions
        except QuizQuestionGroup.DoesNotExist:
            return []

    
    def _generate_fragrance_combinations(self):
        """
        调用AI接口分析用户答题记录，返回主香调和次香调
        """
        # 调用AI接口分析用户答题记录
        try:
            ai_result = self._call_fragrance_ai()
            # print(ai_result)
            # 解析AI返回的结果
            main_fragrance = ai_result.get('主香调')  # 默认值
            secondary_fragrance = ai_result.get('次香调')  # 默认值
            
            # 构建返回结果
            result = {
                'main_fragrance': main_fragrance,
                'secondary_fragrance': secondary_fragrance,
                'main_images': [],  # 由前端填充
                'secondary_images': []  # 由前端填充
            }
            
            return result
            
        except Exception as e:
            # 如果AI接口调用失败，使用默认值
            print(f"AI接口调用失败: {e}")
            return {
                'main_fragrance': '柑橘类',
                'secondary_fragrance': '花卉类',  # 确保与数据库中的类别完全匹配
                'main_images': [],
                'secondary_images': []
            }
    
    def _call_fragrance_ai(self):
        """
        调用AI接口分析用户答题记录，返回主香调和次香调
        这里是一个模拟实现，实际应用中需要替换为真实的AI接口调用
        """
        # print("正在调用AI接口...")
        
        # 获取用户会话
        session = UserQuizSession.objects.filter(
            user=self.request.user,
            status='in_progress'
        ).first()
        
        if not session:
            print("未找到有效的用户会话")
            # 根据用户偏好确定主香调和次香调
            main_fragrance = '柑橘类'  # 默认值
            secondary_fragrance = '花卉类（除白色花卉）'  # 默认值，确保与数据库中的类别完全匹配
            
            return {
                '主香调': main_fragrance,
                '次香调': secondary_fragrance
            }
        
        # 获取用户前三个部分的答案
        user_answers = UserAnswer.objects.filter(
            session=session,
            part__in=[1, 2, 3]
        ).select_related('question').prefetch_related('question__options')
        
        # 构建问题和答案的字典对
        question_answer_dict = {}
        
        for answer in user_answers:
            question = answer.question
            question_text = question.text
            
            # 根据题目类型处理答案
            if question.type in ['single', 'image-single']:  # 单选题
                try:
                    value = json.loads(answer.value) if answer.value else None
                    # 获取选项文本
                    if value:
                        option = question.options.filter(value=value).first()
                        answer_text = option.label if option else value
                    else:
                        answer_text = None
                except json.JSONDecodeError:
                    answer_text = answer.value
                    
            elif question.type in ['multiple', 'image-multiple']:  # 多选题
                try:
                    values = json.loads(answer.value) if answer.value else []
                    # 获取选项文本列表
                    answer_texts = []
                    if values:
                        for value in values:
                            option = question.options.filter(value=value).first()
                            if option:
                                answer_texts.append(option.label)
                            else:
                                answer_texts.append(value)
                    answer_text = answer_texts
                except json.JSONDecodeError:
                    answer_text = answer.value
                    
            elif question.type in ['text', 'single-with-text']:  # 填空题或单选加填空
                answer_text = answer.text if answer.text else answer.value
                
            else:  # 其他类型
                answer_text = answer.value
            
            # 添加到字典
            question_answer_dict[question_text] = answer_text
        
        # 限制为前20题
        if len(question_answer_dict) > 20:
            # 转换为列表，取前20个，再转回字典
            items = list(question_answer_dict.items())[:20]
            question_answer_dict = dict(items)
        
        # print("问题和答案字典对:", question_answer_dict)

        from http import HTTPStatus
        from dashscope import Application

        dashscope_api_key = getattr(settings, 'DASHSCOPE_API_KEY', '')
        if not dashscope_api_key:
            return Response(
                {'detail': '阿里云百炼API密钥未配置。'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=dashscope_api_key,
            app_id='6e85e84a55ef4b5ea41b197077a159c6',  # 替换为实际的应用 ID
            prompt=str(question_answer_dict))

        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
            print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
        else:
            # print(response.output.text)
            pass

        result_dict = json.loads(response.output.text)
        return result_dict

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
            
            # 构建返回数据，与其他部分格式保持一致
            return_data = {
                'id': group.id,
                'title': group.title,
                'description': group.description,
                'questions': serializer.data,
                'mainFragrance': session.main_fragrance or '柑橘类',
                'secondaryFragrance': session.secondary_fragrance or '蔬果类'
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

# 用于分析用户答题记录并返回主香调和次香调的视图
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_fragrance_preferences(request):
    """分析用户答题记录，返回主香调和次香调"""
    pass

def _get_fragrance_images(category_type):
    """
    根据香调类别获取图片列表
    """
    try:
        # 从数据库中获取指定类别的所有香调图片
        fragrance_categories = FragranceCategory.objects.filter(category_type=category_type)
        
        # 提取图片URL列表
        images = []
        for category in fragrance_categories:
            if category.image_url:
                # 获取图片文件名作为标签
                image_path = category.image_url
                image_name = image_path.split('/')[-1].split('.')[0]  # 去掉扩展名
                images.append({
                    'label': image_name,
                    'value': image_path,
                    'image': image_path
                })
        
        return images
    except Exception as e:
        print(f"获取香调图片失败: {str(e)}")
        return []

# 获取香调类别图片列表的API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fragrance_images(request):
    """获取指定香调类别的图片列表"""
    try:
        category_type = request.query_params.get('category_type')
        if not category_type:
            return Response(
                {'detail': '香调类别不能为空。'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取指定类别的图片列表
        images = _get_fragrance_images(category_type)
        
        return Response({
            'category_type': category_type,
            'images': images
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        # 记录错误日志
        print(f"获取香调图片失败: {str(e)}")
        return Response(
            {'detail': f'获取香调图片失败，请稍后重试。错误信息：{str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )