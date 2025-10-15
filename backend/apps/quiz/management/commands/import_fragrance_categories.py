from django.core.management.base import BaseCommand
from apps.quiz.models import FragranceCategory
import csv
import os
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = '导入香调类别数据'

    def handle(self, *args, **options):
        """导入香调类别数据"""
        # 获取CSV文件路径
        csv_file_path = os.path.join(os.path.dirname(__file__), 'fragrance_category.csv')
        
        # 检查文件是否存在
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV文件不存在: {csv_file_path}"))
            return
        
        # 导入数据
        created_count = 0
        updated_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # 准备数据字典
                data = {
                    'id': row['id'],
                    'name': row['name'],
                    'english_name': row['english_name'],
                    'core_trait_1': row['core_trait_1'],
                    'core_trait_2': row['core_trait_2'],
                    'intensity': row['intensity'],
                    'style_keywords': row['style_keywords'],
                    'image_url': row['image_url'],
                    'category_type': row['category_type']
                }
                
                # 处理创建和更新时间
                if row.get('created_at'):
                    try:
                        data['created_at'] = parse_datetime(row['created_at'])
                    except:
                        pass
                
                if row.get('updated_at'):
                    try:
                        data['updated_at'] = parse_datetime(row['updated_at'])
                    except:
                        pass
                
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
        
        self.stdout.write(self.style.SUCCESS(f"香调数据导入完成！"))
        self.stdout.write(self.style.SUCCESS(f"创建记录数: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"更新记录数: {updated_count}"))