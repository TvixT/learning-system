from django.core.management.base import BaseCommand
from courses.models import Category, Tag


class Command(BaseCommand):
    help = 'Populate the database with sample categories and tags'

    def handle(self, *args, **options):
        # Create sample categories
        categories = [
            'Programming',
            'Data Science',
            'Web Development',
            'Mobile Development',
            'Database Management',
            'Cloud Computing',
            'Cybersecurity',
            'Artificial Intelligence',
            'Machine Learning',
            'DevOps'
        ]
        
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(f'Created category: {category_name}')
            else:
                self.stdout.write(f'Category already exists: {category_name}')
        
        # Create sample tags
        tags = [
            'Python',
            'JavaScript',
            'Java',
            'C++',
            'SQL',
            'NoSQL',
            'React',
            'Vue',
            'Angular',
            'Django',
            'Flask',
            'Node.js',
            'Express',
            'MongoDB',
            'PostgreSQL',
            'MySQL',
            'AWS',
            'Azure',
            'Docker',
            'Kubernetes'
        ]
        
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')
            else:
                self.stdout.write(f'Tag already exists: {tag_name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated categories and tags')
        )