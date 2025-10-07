# import_questions.py

from django.core.management.base import BaseCommand
from apps.quiz.models import QuizQuestionGroup, QuizQuestion, QuizQuestionOption

class Command(BaseCommand):
    help = 'Import quiz questions from predefined data structure'

    def handle(self, *args, **options):
        # 完全匹配前端的题目数据
        question_groups = [
            # ============ Part 1: 多个单选题 ============
            {
                "id": "part1",
                "title": "🌿 情景选择",
                "description": "基于大五人格的香水偏好测试",
                "questions": [
                    {
                        "id": "q1-1",
                        "text": "一个漫长的项目终于结束，你有了一周完整的假期。你会如何安排？",
                        "type": "single",
                        "options": [
                            {"label": "开启一次短途旅行，去探索一个从未去过的自然景点或城市。", "value": "A", "emoji": "🌍"},
                            {"label": "在家彻底放松，看书、看电影，或是为自己做几顿精致的美食。", "value": "B", "emoji": "🛋️"},
                            {"label": "和朋友聚会、开派对，或者去参加一些热闹的社交活动。", "value": "C", "emoji": "🎉"},
                            {"label": "借此机会整理房间、做一次大扫除，或是为下一个项目做初步规划。", "value": "D", "emoji": "🧹"},
                            {"label": "需要几天时间什么都不做，彻底放空，来缓解项目积累的疲惫和压力。", "value": "E", "emoji": "🧘"}
                        ]
                    },
                    {
                        "id": "q1-2",
                        "text": "你收到一份包装精美的礼物，你的第一反应是？",
                        "type": "single",
                        "options": [
                            {"label": "欣赏包装的创意与美学，猜测里面会是什么有趣的东西。", "value": "A", "emoji": "🎁"},
                            {"label": "感到温暖和感激，立刻想到送礼物的人的心意。", "value": "B", "emoji": "💌"},
                            {"label": "非常兴奋和好奇，迫不及待地想打开它。", "value": "C", "emoji": "🤩"},
                            {"label": "小心翼翼地拆开包装，尽量不破坏包装纸，以便收藏或再利用。", "value": "D", "emoji": "✂️"},
                            {"label": "有点意外和不知所措，担心礼物太贵重不知道如何回礼。", "value": "E", "emoji": "😳"}
                        ]
                    },
                    {
                        "id": "q1-3",
                        "text": "在布置你的个人空间（卧室或书房）时，你更看重？",
                        "type": "single",
                        "options": [
                            {"label": "独特有格调的艺术品、书籍和旅行纪念品，展现个性。", "value": "A", "emoji": "🖼️"},
                            {"label": "舒适温馨的氛围，柔软的毯子、温暖的灯光和家人的照片。", "value": "B", "emoji": "🕯️"},
                            {"label": "明亮活泼的色彩，适合朋友来聚会聊天，充满活力。", "value": "C", "emoji": "🌈"},
                            {"label": "整洁、高效和功能性，每样东西都有其固定的位置，一目了然。", "value": "D", "emoji": "🗄️"},
                            {"label": "一个能让我完全放松、有安全感、隔绝外界打扰的“避难所”。", "value": "E", "emoji": "🛌"}
                        ]
                    },
                    {
                        "id": "q1-4",
                        "text": "朋友向你倾诉烦恼，你的回应方式更倾向于？",
                        "type": "single",
                        "options": [
                            {"label": "帮他分析问题，提供各种不同的视角和解决方案。", "value": "A", "emoji": "💡"},
                            {"label": "耐心倾听，给予情感上的支持和安慰，让他感到被理解。", "value": "B", "emoji": "🤗"},
                            {"label": "带他出去散心，用轻松愉快的事情转移注意力，帮他振作起来。", "value": "C", "emoji": "🎢"},
                            {"label": "给出清晰、有条理的建议，甚至想帮他规划下一步该怎么做。", "value": "D", "emoji": "📋"},
                            {"label": "会非常共情他的痛苦，甚至可能让自己的情绪也受到影响，变得有些低落。", "value": "E", "emoji": "💧"}
                        ]
                    },
                    {
                        "id": "q1-5",
                        "text": "在一次团队讨论中，你通常扮演的角色是？",
                        "type": "single",
                        "options": [
                            {"label": "提出新奇点子、新颖视角和可能性、打破常规的“创意引擎”。", "value": "A", "emoji": "🚀"},
                            {"label": "调解分歧、促进和谐合作与团队凝聚力的“和谐粘合剂”。", "value": "B", "emoji": "🤝"},
                            {"label": "推动交流，活跃讨论气氛的“氛围催化剂”。", "value": "C", "emoji": "🎤"},
                            {"label": "注重条理性与细节、确保项目有序推进的“架构师”。", "value": "D", "emoji": "📐"},
                            {"label": "容易察觉到团队中的紧张气氛或担忧潜在隐患的“风险雷达”。", "value": "E", "emoji": "⚠️"}
                        ]
                    },
                    {
                        "id": "q1-6",
                        "text": "当你选择日常穿着时，哪一个才是你最优先的考量？",
                        "type": "single",
                        "options": [
                            {"label": "这么穿能表达我的独特风格吗？", "value": "A", "emoji": "🕶️"},
                            {"label": "这么穿会让别人感到不舒服吗？", "value": "B", "emoji": "👗"},
                            {"label": "这么穿能帮我获得关注吗？", "value": "C", "emoji": "👑"},
                            {"label": "这么穿适合今天的场合吗？", "value": "D", "emoji": "👔"},
                            {"label": "这么穿能避免任何不必要的关注或批评吗？", "value": "E", "emoji": "🧥"}
                        ]
                    },
                    {
                        "id": "q1-7",
                        "text": "如果用一个词来形容你想要的生活，它更接近？",
                        "type": "single",
                        "options": [
                            {"label": "精彩", "value": "A", "emoji": "🎬"},
                            {"label": "和睦", "value": "B", "emoji": "🏡"},
                            {"label": "热闹", "value": "C", "emoji": "🎪"},
                            {"label": "有序", "value": "D", "emoji": "📅"},
                            {"label": "安稳", "value": "E", "emoji": "🛡️"}
                        ]
                    },
                    {
                        "id": "q1-8",
                        "text": "对“传统”的看法",
                        "type": "single",
                        "options": [
                            {"label": "它是创新的基石，我乐于在传统基础上打破常规，探索新形式。", "value": "A", "emoji": "🧱"},
                            {"label": "当遵循传统能促进人与人之间的和谐与连接时，我会感到非常温暖和舒适。", "value": "B", "emoji": "🏮"},
                            {"label": "它如果能带来集体欢庆的氛围，让聚会更有趣，那就太好了！", "value": "C", "emoji": "🎊"},
                            {"label": "它是经过时间检验的有效行为准则，遵循它让生活更有序可靠。", "value": "D", "emoji": "📜"},
                            {"label": "它有时是一种负担，我会担心自己做得不够好，让家人失望。", "value": "E", "emoji": "😰"}
                        ]
                    },
                    {
                        "id": "q1-9",
                        "text": "当你感到压力巨大或焦虑时，你最渴望做什么？",
                        "type": "single",
                        "options": [
                            {"label": "独自探索一个能激发新想法的地方（如美术馆、大自然），用全新的视角取代焦虑。", "value": "A", "emoji": "🏞️"},
                            {"label": "与一位能给你安全感的朋友或家人深度交谈，寻求安慰。", "value": "B", "emoji": "💬"},
                            {"label": "立刻找朋友出去玩，用热闹和欢乐把自己从情绪中“拽”出来。", "value": "C", "emoji": "🍹"},
                            {"label": "制定一个详细的计划列表，一步步解决问题，重新获得控制感。", "value": "D", "emoji": "✅"},
                            {"label": "把自己封闭在一个绝对安全的环境里，通过舒缓仪式（如泡澡等）来隔绝外界压力。", "value": "E", "emoji": "🛁"}
                        ]
                    },
                    {
                        "id": "q1-10",
                        "text": "面对一个突如其来的批评或挫折，你内心的第一反应更接近？",
                        "type": "single",
                        "options": [
                            {"label": "这很有趣，Ta为什么这么看？这背后有什么原因？", "value": "A", "emoji": "🧐"},
                            {"label": "我是不是让Ta失望了？我真希望我们能和睦相处。", "value": "B", "emoji": "🥺"},
                            {"label": "真烦人，不想了，走，干别的事去！", "value": "C", "emoji": "🏃"},
                            {"label": "我需要评估这个批评的有效性，并列出改进的步骤。", "value": "D", "emoji": "📊"},
                            {"label": "我果然什么都做不好，一切都糟透了。", "value": "E", "emoji": "😔"}
                        ]
                    }
                ]
            },
            
            # ============ Part 2: 单选 + 条件填空 ===========
            {
                "id": "part2",
                "title": "👃 感官敏感度测试：浓香 or 淡香？",
                "description": "通过日常气味体验，判断你对香气的敏感程度，帮助推荐最适合你的香氛浓度",
                "questions": [
                    {
                        "id": "q2-1",
                        "text": "当你走进一家咖啡馆，或者早上自己冲煮一杯新鲜咖啡时，你通常能多清晰地闻到咖啡的香气？",
                        "type": "single",
                        "options": [
                            {"label": "非常清晰 - 能立刻闻到浓郁、令人愉悦的咖啡醇香，甚至能分辨出不同豆子的风味。", "value": "A", "emoji": "☕️"},
                            {"label": "比较清晰 - 能明显闻到咖啡味，但不会觉得特别强烈。", "value": "B", "emoji": "🙂"},
                            {"label": "比较微弱 - 需要刻意去闻，或者靠近了才能闻到。", "value": "C", "emoji": "🤔"},
                            {"label": "几乎闻不到 - 别人都说很香，但我几乎闻不到什么气味。", "value": "D", "emoji": "😶"}
                        ]
                    },
                    {
                        "id": "q2-2",
                        "text": "当你挑选一个柠檬或橙子时，你通常需要多近才能通过气味判断它的新鲜度？",
                        "type": "single",
                        "options": [
                            {"label": "无需靠近 - 拿起它时，在正常距离下就能闻到清新的果皮香气。", "value": "A", "emoji": "🍋"},
                            {"label": "稍近一些 - 需要拿到离鼻子10-15厘米左右才能清晰闻到。", "value": "B", "emoji": "👃"},
                            {"label": "非常近 - 需要凑得很近，几乎贴到鼻子上才能闻到一丝气味。", "value": "C", "emoji": "🔍"},
                            {"label": "闻不到 - 即使切开，也很难闻到其特有的酸爽清香。", "value": "D", "emoji": "🚫"}
                        ]
                    },
                    {
                        "id": "q2-3",
                        "text": "在使用一块新的花香或果香味的香皂沐浴后，你身上的留香情况如何？",
                        "type": "single",
                        "options": [
                            {"label": "持久留香 - 沐浴后1-2小时内，自己和他人都能清晰闻到淡淡的清香。", "value": "A", "emoji": "🌸"},
                            {"label": "短暂留香 - 刚沐浴完时自己能闻到，但很快气味就消散了。", "value": "B", "emoji": "💨"},
                            {"label": "非常微弱 - 只有在抬起手臂等特定动作时，自己才能隐约闻到一点。", "value": "C", "emoji": "🫧"},
                            {"label": "几乎没有 - 从来看不到别人“闻起来很香”的评价，自己也很少察觉到。", "value": "D", "emoji": "🧼"}
                        ]
                    },
                    {
                        "id": "q2-4",
                        "text": "当你在家煎炸食物（如煎 bacon、炸花生米）后，厨房的气味会持续多久？",
                        "type": "single",
                        "options": [
                            {"label": "敏感者 - 气味非常顽固，即使开窗通风，第二天还能隐约闻到。", "value": "A", "emoji": "🤢"},
                            {"label": "普通者 - 通风几个小时后，气味就基本消散了。", "value": "B", "emoji": "🌬️"},
                            {"label": "迟钝者 - 做完饭通风一会儿就感觉没味道了，有时家人说还有味，但我闻不到。", "value": "C", "emoji": "🤷‍♀️"},
                            {"label": "无感者 - 很少注意到厨房有特殊的残留气味。", "value": "D", "emoji": "😐"}
                        ]
                    },
                    {
                        "id": "q2-5",
                        "text": "在一场小雨过后，你走过公园的草地或花园，你能闻到什么？",
                        "type": "single",
                        "options": [
                            {"label": "丰富的层次 - 能清晰地闻到泥土的湿润气息、青草的清新味，甚至还有花香。", "value": "A", "emoji": "🌿🌧️"},
                            {"label": "淡淡的清新 - 主要能闻到一股清新的空气和淡淡的泥土味。", "value": "B", "emoji": "🍃"},
                            {"label": "极其微弱 - 需要非常努力地深呼吸，才能感觉到一丝不一样。", "value": "C", "emoji": "😮‍💨"},
                            {"label": "毫无区别 - 和平时空气的味道没什么不同，闻不到所谓的“雨后清香”。", "value": "D", "emoji": "🌫️"}
                        ]
                    },
                    {
                        "id": "q2-6",
                        "text": "与他人相比，您觉得自己的鼻子灵敏吗？",
                        "type": "single",
                        "options": [
                            {"label": "比大多数人灵敏得多", "value": "A", "emoji": "🐕"},
                            {"label": "比大多数人稍微灵敏一点", "value": "B", "emoji": "👃"},
                            {"label": "和大多数人差不多", "value": "C", "emoji": "🙂"},
                            {"label": "比大多数人稍微迟钝一点", "value": "D", "emoji": "🧐"},
                            {"label": "比大多数人迟钝得多", "value": "E", "emoji": "😴"}
                        ]
                    },
                    {
                        "id": "q2-7",
                        "text": "在以下场景中，您对他人身上过浓的香水味反应是？",
                        "type": "single",
                        "options": [
                            {"label": "非常反感，感到头晕不适", "value": "A", "emoji": "😵‍💫"},
                            {"label": "有点不舒服，会刻意避开", "value": "B", "emoji": "😷"},
                            {"label": "无所谓，不太在意", "value": "C", "emoji": "😶"},
                            {"label": "挺喜欢的，会注意到香味", "value": "D", "emoji": "😍"}
                        ]
                    },
                    {
                        "id": "q2-8",
                        "text": "您平时如何使用香水？（可多选）",
                        "type": "multiple",
                        "options": [
                            {"label": "只喷一下在手腕/颈部", "value": "A", "emoji": "🧴"},
                            {"label": "3下在不同部位", "value": "B", "emoji": "✨"},
                            {"label": "会喷洒在衣物上", "value": "C", "emoji": "👕"},
                            {"label": "喜欢大面积喷洒营造氛围", "value": "D", "emoji": "🎭"},
                            {"label": "不确定/看心情", "value": "E", "emoji": "🎲"}
                        ]
                    },
                    {
                        "id": "q2-9",
                        "text": "您常用的香水是：",
                        "type": "single-with-text",
                        "showTextWhen": "yes",
                        "textFollowUp": "请列出您常用的香水：",
                        "placeholder": "例如：迪奥真我、香奈儿5号...",
                        "options": [
                            {"label": "有使用过", "value": "yes", "emoji": "✅"},
                            {"label": "从未使用", "value": "no", "emoji": "❌"}
                        ]
                    }
                ]
            },
            
            # ============ Part 3: 填空题 ============
            {
                "id": "part3",
                "title": "🖼️ 感官具象化场景",
                "description": "请使用文字描述一个让你感受到放松的场景",
                "questions": [
                    {
                        "id": "q3",
                        "text": "请尽可能的详细描述让你感受到放松的场景",
                        "type": "text"
                    }
                ]
            },
            
            # ============ Part 4: 报告类题目（动态生成选项） ============
            {
                "id": "part4",
                "title": "香调偏好报告",
                "description": "根据您的回答生成的个性化香调推荐",
                "questions": [
                    {
                        "id": "q4",
                        "text": "根据您的回答，以下哪些香调组合最适合您？（可多选）",
                        "type": "image-multiple",
                        "image_range": True,  # 图片选项
                        "images_path": "/images/smell/",  # 图片路径
                        "min_selection": 1,
                        "max_selection": 3,
                        "options": []  # 选项将由后端动态生成
                    }
                ]
            }
        ]

        # 导入题目数据
        for group_data in question_groups:
            # 创建题目组
            group, created = QuizQuestionGroup.objects.update_or_create(
                id=group_data['id'],
                defaults={
                    'title': group_data['title'],
                    'description': group_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created question group: {group.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated question group: {group.title}'))

            # 创建题目
            for i, question_data in enumerate(group_data['questions']):
                # 构建题目默认值字典
                question_defaults = {
                    'group': group,
                    'text': question_data['text'],
                    'type': question_data['type'],
                    'sort_order': i,
                    'show_text_when': question_data.get('showTextWhen', None),
                    # 根据题目类型设置默认的最小和最大选择数
                    'min_selection': question_data.get('minSelection', 1),
                    'max_selection': question_data.get('maxSelection', 
                        3 if question_data['type'] in ['multiple', 'image-multiple'] else 1
                    )
                }
                
                # 创建题目
                question, created = QuizQuestion.objects.update_or_create(
                    id=question_data['id'],
                    defaults=question_defaults
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created question: {question.text}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'  Updated question: {question.text}'))

                # 只对有选项的题目类型创建选项
                if 'options' in question_data:
                    for j, option_data in enumerate(question_data['options']):
                        option, created = QuizQuestionOption.objects.update_or_create(
                            question=question,
                            value=option_data['value'],
                            defaults={
                                'label': option_data['label'],
                                'emoji': option_data.get('emoji', ''),
                                'sort_order': j
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'    Created option: {option.value} - {option.label}'))

        self.stdout.write(self.style.SUCCESS('All questions imported successfully!'))