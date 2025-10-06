# quiz/fragrance_analysis.py

from django.db.models import Count
from .models import UserAnswer, FragranceCategory


def analyze_fragrance_preferences(user_answers, top_n=6):
    return get_default_fragrance_categories()
    """
    根据用户答案分析香调偏好
    
    参数:
        user_answers: 用户答案列表或字典
        top_n: 返回的香调偏好数量
        
    返回:
        list: 排序后的香调偏好列表，每个元素包含香调信息和匹配分数
    """
    # 示例实现：这里使用简化的匹配算法
    # 在实际应用中，应该根据题目设计和香调分类进行更复杂的分析
    
    # 初始化香调偏好分数字典
    category_scores = {
        'floral': {'score': 0, 'category': '花卉类（除白色花卉）'},  # 花香调
        'white_floral': {'score': 0, 'category': '白色花卉'},  # 白色花香调
        'woody': {'score': 0, 'category': '树木、苔藓'},  # 木质调
        'citrus': {'score': 0, 'category': '柑橘类'},  # 柑橘调
        'spicy': {'score': 0, 'category': '辛香料'},  # 辛辣调
        'green': {'score': 0, 'category': '草本、绿叶'},  # 草本绿叶调
        'resin': {'score': 0, 'category': '树脂'},  # 树脂调
        'fruit_vegetable': {'score': 0, 'category': '蔬果类'},  # 蔬果调
        'other': {'score': 0, 'category': '其他'}  # 其他调
    }
    
    # 简单的答案分析逻辑
    # 在实际应用中，这里应该根据具体的题目设计和答案内容进行更复杂的分析
    for answer in user_answers.values():
        # 检查答案是否包含关键词或特定选项
        if isinstance(answer, dict):
            answer_text = answer.get('text', '')
            answer_value = answer.get('value', '')
        else:
            answer_text = str(answer)
            answer_value = str(answer)
        
        # 分析文本答案中的关键词
        text_lower = (answer_text + ' ' + answer_value).lower()
        
        # 为不同的香调类别分配分数
        if any(word in text_lower for word in ['花', '花香', '玫瑰', '茉莉', '百合']):
            category_scores['floral']['score'] += 2
            category_scores['white_floral']['score'] += 1
        if any(word in text_lower for word in ['木', '木质', '雪松', '檀香', '橡木']):
            category_scores['woody']['score'] += 2
        if any(word in text_lower for word in ['柑橘', '柠檬', '橙子', '柚子', '香茅']):
            category_scores['citrus']['score'] += 2
        if any(word in text_lower for word in ['辛辣', '胡椒', '姜', '肉桂', '丁香']):
            category_scores['spicy']['score'] += 2
        if any(word in text_lower for word in ['草本', '绿叶', '青草', '薄荷', '艾草']):
            category_scores['green']['score'] += 2
        if any(word in text_lower for word in ['树脂', '乳香', '没药', '安息香', '焚香']):
            category_scores['resin']['score'] += 2
        if any(word in text_lower for word in ['水果', '蔬菜', '果香', '甜', '酸']):
            category_scores['fruit_vegetable']['score'] += 2
    
    # 从数据库中获取香调类别信息
    fragrance_preferences = []
    for category_id, info in category_scores.items():
        # 获取该类别的代表图片（使用第一个匹配的图片）
        category_obj = FragranceCategory.objects.filter(
            id=category_id,
            category_type=info['category']
        ).first()
        
        if category_obj:
            fragrance_preferences.append({
                'id': category_obj.id,
                'name': category_obj.name,
                'english_name': category_obj.english_name,
                'image_url': category_obj.image_url,
                'category_type': category_obj.category_type,
                'core_trait_1': category_obj.core_trait_1,
                'core_trait_2': category_obj.core_trait_2,
                'intensity': category_obj.intensity,
                'style_keywords': category_obj.style_keywords,
                'score': info['score']
            })
    
    # 按分数排序，返回前N个香调偏好
    fragrance_preferences.sort(key=lambda x: x['score'], reverse=True)
    
    # 如果数据库中没有香调信息，返回默认的香调列表
    if not fragrance_preferences:
        return get_default_fragrance_categories()
    
    return fragrance_preferences[:top_n]


def get_default_fragrance_categories():
    """
    获取默认的香调类别列表
    当数据库中没有香调信息时使用
    现在随机获取数据库表中的数据
    """
    # 尝试从数据库中随机获取最多6个香调类别
    try:
        # 使用order_by('?')来随机排序香调类别
        random_categories = FragranceCategory.objects.order_by('?')[:6]
        
        # 将数据库对象转换为需要的字典格式
        result = []
        for category in random_categories:
            result.append({
                'id': category.id,
                'name': category.name,
                'english_name': category.english_name,
                'image_url': category.image_url,
                'category_type': category.category_type,
                'core_trait_1': category.core_trait_1,
                'core_trait_2': category.core_trait_2,
                'intensity': category.intensity,
                'style_keywords': category.style_keywords,
                'score': 0
            })
        
        # 如果数据库中有数据，返回随机获取的香调类别
        if result:
            return result
    except Exception as e:
        # 发生异常时（例如数据库连接问题），继续返回默认列表
        pass
    
    # 如果数据库中没有数据，返回一个空列表
    return []