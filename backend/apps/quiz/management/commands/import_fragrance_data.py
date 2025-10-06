#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
香调数据导入脚本
使用方法：在Django项目根目录下运行 python -m apps.quiz.import_fragrance_data
"""

import os
import sys

# 确保可以导入Django模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from apps.quiz.models import FragranceCategory


def import_fragrance_categories():
    """导入香调类别数据"""
    # 定义香调类别数据
    fragrance_data = [
        # 花卉类（除白色花卉）
        {
            'id': 'floral', 
            'name': '花香调', 
            'english_name': 'Floral', 
            'core_trait_1': '花香/强', 
            'core_trait_2': '甜美/中等', 
            'intensity': 7, 
            'style_keywords': '浪漫,优雅,女性化', 
            'image_url': '/images/smell/花卉类（除白色花卉）/三叶草.png', 
            'category_type': '花卉类（除白色花卉）'
        },
        {
            'id': 'floral_rose', 
            'name': '玫瑰花香', 
            'english_name': 'Rose', 
            'core_trait_1': '玫瑰/强', 
            'core_trait_2': '花香/强', 
            'intensity': 8, 
            'style_keywords': '浪漫,优雅,经典', 
            'image_url': '/images/smell/花卉类（除白色花卉）/玫瑰.png', 
            'category_type': '花卉类（除白色花卉）'
        },
        {
            'id': 'floral_jasmine', 
            'name': '茉莉花香', 
            'english_name': 'Jasmine', 
            'core_trait_1': '茉莉/强', 
            'core_trait_2': '清新/中等', 
            'intensity': 7, 
            'style_keywords': '优雅,纯净,持久', 
            'image_url': '/images/smell/花卉类（除白色花卉）/茉莉花.png', 
            'category_type': '花卉类（除白色花卉）'
        },
        
        # 白色花卉
        {
            'id': 'white_floral', 
            'name': '白色花香调', 
            'english_name': 'White Floral', 
            'core_trait_1': '白花/强', 
            'core_trait_2': '浓郁/中等', 
            'intensity': 8, 
            'style_keywords': '奢华,馥郁,感性', 
            'image_url': '/images/smell/白色花卉/亚马逊月光花.png', 
            'category_type': '白色花卉'
        },
        {
            'id': 'white_floral_jasmine', 
            'name': '白茉莉', 
            'english_name': 'White Jasmine', 
            'core_trait_1': '茉莉/强', 
            'core_trait_2': '纯净/中等', 
            'intensity': 7, 
            'style_keywords': '纯净,优雅,清新', 
            'image_url': '/images/smell/白色花卉/茉莉.png', 
            'category_type': '白色花卉'
        },
        {
            'id': 'white_floral_tuberose', 
            'name': '晚香玉', 
            'english_name': 'Tuberose', 
            'core_trait_1': '晚香玉/强', 
            'core_trait_2': '浓郁/强', 
            'intensity': 9, 
            'style_keywords': '奢华,馥郁,性感', 
            'image_url': '/images/smell/白色花卉/晚香玉.png', 
            'category_type': '白色花卉'
        },
        
        # 树木、苔藓
        {
            'id': 'woody', 
            'name': '木质调', 
            'english_name': 'Woody', 
            'core_trait_1': '木质/强', 
            'core_trait_2': '温暖/中等', 
            'intensity': 7, 
            'style_keywords': '稳重,自然,持久', 
            'image_url': '/images/smell/树木、苔藓/云杉.png', 
            'category_type': '树木、苔藓'
        },
        {
            'id': 'woody_sandalwood', 
            'name': '檀香木', 
            'english_name': 'Sandalwood', 
            'core_trait_1': '檀香/强', 
            'core_trait_2': '温暖/强', 
            'intensity': 8, 
            'style_keywords': '神秘,东方,持久', 
            'image_url': '/images/smell/树木、苔藓/檀香木.png', 
            'category_type': '树木、苔藓'
        },
        {
            'id': 'woody_cedar', 
            'name': '雪松', 
            'english_name': 'Cedarwood', 
            'core_trait_1': '雪松/强', 
            'core_trait_2': '清新/中等', 
            'intensity': 7, 
            'style_keywords': '自然,干净,男性化', 
            'image_url': '/images/smell/树木、苔藓/雪松.png', 
            'category_type': '树木、苔藓'
        },
        
        # 柑橘类
        {
            'id': 'citrus', 
            'name': '柑橘调', 
            'english_name': 'Citrus', 
            'core_trait_1': '柑橘/强', 
            'core_trait_2': '清新/强', 
            'intensity': 6, 
            'style_keywords': '活力,清爽,明快', 
            'image_url': '/images/smell/柑橘类/克里曼丁红橘.png', 
            'category_type': '柑橘类'
        },
        {
            'id': 'citrus_lemon', 
            'name': '柠檬', 
            'english_name': 'Lemon', 
            'core_trait_1': '柠檬/强', 
            'core_trait_2': '清新/强', 
            'intensity': 6, 
            'style_keywords': '清新,活力,提神', 
            'image_url': '/images/smell/柑橘类/柠檬.png', 
            'category_type': '柑橘类'
        },
        {
            'id': 'citrus_orange', 
            'name': '橙子', 
            'english_name': 'Orange', 
            'core_trait_1': '橙子/强', 
            'core_trait_2': '甜美/中等', 
            'intensity': 6, 
            'style_keywords': '阳光,活力,开朗', 
            'image_url': '/images/smell/柑橘类/橙子.png', 
            'category_type': '柑橘类'
        },
        
        # 辛香料
        {
            'id': 'spicy', 
            'name': '辛辣调', 
            'english_name': 'Spicy', 
            'core_trait_1': '辛辣/强', 
            'core_trait_2': '温暖/强', 
            'intensity': 8, 
            'style_keywords': '热情,神秘,东方', 
            'image_url': '/images/smell/辛香料/八角.png', 
            'category_type': '辛香料'
        },
        {
            'id': 'spicy_cinnamon', 
            'name': '肉桂', 
            'english_name': 'Cinnamon', 
            'core_trait_1': '肉桂/强', 
            'core_trait_2': '温暖/强', 
            'intensity': 8, 
            'style_keywords': '温暖,甜辣,节日', 
            'image_url': '/images/smell/辛香料/肉桂.png', 
            'category_type': '辛香料'
        },
        {
            'id': 'spicy_pepper', 
            'name': '胡椒', 
            'english_name': 'Pepper', 
            'core_trait_1': '胡椒/强', 
            'core_trait_2': '辛辣/强', 
            'intensity': 9, 
            'style_keywords': '辛辣,刺激,男性化', 
            'image_url': '/images/smell/辛香料/胡椒.png', 
            'category_type': '辛香料'
        },
        
        # 草本、绿叶
        {
            'id': 'green', 
            'name': '草本绿叶调', 
            'english_name': 'Green', 
            'core_trait_1': '草本/强', 
            'core_trait_2': '绿叶/强', 
            'intensity': 6, 
            'style_keywords': '自然,清爽,新鲜', 
            'image_url': '/images/smell/草本、绿叶/不凋花.png', 
            'category_type': '草本、绿叶'
        },
        {
            'id': 'green_mint', 
            'name': '薄荷', 
            'english_name': 'Mint', 
            'core_trait_1': '薄荷/强', 
            'core_trait_2': '清凉/强', 
            'intensity': 7, 
            'style_keywords': '清凉,提神,干净', 
            'image_url': '/images/smell/草本、绿叶/薄荷.png', 
            'category_type': '草本、绿叶'
        },
        {
            'id': 'green_grass', 
            'name': '青草', 
            'english_name': 'Grass', 
            'core_trait_1': '青草/强', 
            'core_trait_2': '自然/强', 
            'intensity': 6, 
            'style_keywords': '清新,自然,纯净', 
            'image_url': '/images/smell/草本、绿叶/青草.png', 
            'category_type': '草本、绿叶'
        },
        
        # 树脂
        {
            'id': 'resin', 
            'name': '树脂调', 
            'english_name': 'Resinous', 
            'core_trait_1': '树脂/强', 
            'core_trait_2': '温暖/强', 
            'intensity': 8, 
            'style_keywords': '持久,温暖,东方', 
            'image_url': '/images/smell/树脂/乳香.png', 
            'category_type': '树脂'
        },
        {
            'id': 'resin_incense', 
            'name': '焚香', 
            'english_name': 'Incense', 
            'core_trait_1': '焚香/强', 
            'core_trait_2': '神秘/中等', 
            'intensity': 8, 
            'style_keywords': '神秘,宗教,东方', 
            'image_url': '/images/smell/树脂/焚香.png', 
            'category_type': '树脂'
        },
        {
            'id': 'resin_myrrh', 
            'name': '没药', 
            'english_name': 'Myrrh', 
            'core_trait_1': '没药/强', 
            'core_trait_2': '温暖/中等', 
            'intensity': 7, 
            'style_keywords': '温暖,神秘,持久', 
            'image_url': '/images/smell/树脂/没药.png', 
            'category_type': '树脂'
        },
        
        # 其他
        {
            'id': 'other_amber', 
            'name': '琥珀', 
            'english_name': 'Amber', 
            'core_trait_1': '琥珀/强', 
            'core_trait_2': '温暖/强', 
            'intensity': 8, 
            'style_keywords': '温暖,甜美,持久', 
            'image_url': '/images/smell/其他/琥珀.jpg', 
            'category_type': '其他'
        },
        {
            'id': 'other_vanilla', 
            'name': '香草', 
            'english_name': 'Vanilla', 
            'core_trait_1': '香草/强', 
            'core_trait_2': '甜美/强', 
            'intensity': 7, 
            'style_keywords': '甜美,温暖,舒适', 
            'image_url': '/images/smell/其他/香草.jpg', 
            'category_type': '其他'
        },
        {
            'id': 'other_musk', 
            'name': '麝香', 
            'english_name': 'Musk', 
            'core_trait_1': '麝香/中等', 
            'core_trait_2': '动物感/中等', 
            'intensity': 7, 
            'style_keywords': '性感,温暖,持久', 
            'image_url': '/images/smell/其他/龙涎香.jpg', 
            'category_type': '其他'
        }
    ]
    
    # 导入数据
    created_count = 0
    updated_count = 0
    
    for data in fragrance_data:
        # 检查是否已存在该香调类别
        existing_category = FragranceCategory.objects.filter(id=data['id']).first()
        
        if existing_category:
            # 更新现有记录
            for key, value in data.items():
                setattr(existing_category, key, value)
            existing_category.save()
            updated_count += 1
        else:
            # 创建新记录
            FragranceCategory.objects.create(**data)
            created_count += 1
    
    print(f"香调数据导入完成！")
    print(f"创建记录数: {created_count}")
    print(f"更新记录数: {updated_count}")


if __name__ == "__main__":
    import_fragrance_categories()