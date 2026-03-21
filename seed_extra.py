import os
import django
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churchsite.settings')
django.setup()

from pages.models import ProgramCategory, Program, SuccessStory, NewsStory

def download_image(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(url).path)
            if not file_name or '.' not in file_name:
                file_name = "image.jpg"
            return ContentFile(response.content, name=file_name)
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return None

def seed_extra():
    print("Seeding Programs and Success Stories data...")

    # Categories
    ProgramCategory.objects.all().delete()
    cat_foundation = ProgramCategory.objects.create(
        title='Community Foundation',
        description='Direct support for families and individuals in our local area.',
        icon_svg='M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
        order=1
    )
    cat_edu = ProgramCategory.objects.create(
        title='Education & Skills',
        description='Empowering the next generation through learning and development.',
        icon_svg='M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
        order=2
    )

    # Programs
    Program.objects.all().delete()
    programs_data = [
        {
            'category': cat_foundation,
            'title': 'Weekly Food Bank',
            'slug': 'weekly-food-bank',
            'description': 'Our flagship program providing nutritious groceries to over 500 families every Saturday.',
            'image_url': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
            'tag': 'Weekly',
            'benefit_metric': '500+ families/week',
            'is_featured': True,
            'order': 1
        },
        {
            'category': cat_edu,
            'title': 'Youth Coding Academy',
            'slug': 'youth-coding-academy',
            'description': 'Teaching software development and digital literacy to underprivileged teens.',
            'image_url': 'https://images.unsplash.com/photo-1484417894907-623942c8ee29?w=800',
            'tag': '12 Weeks',
            'benefit_metric': '80% placement rate',
            'is_featured': True,
            'order': 2
        },
        {
            'category': cat_foundation,
            'title': 'Homeless Care Kits',
            'slug': 'homeless-care-kits',
            'description': 'Distributed nightly, these kits contain essential hygiene items and information.',
            'image_url': 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?w=800',
            'tag': 'Daily',
            'benefit_metric': '200+ kits daily',
            'is_featured': False,
            'order': 3
        }
    ]

    for p_data in programs_data:
        p = Program.objects.create(
            category=p_data['category'],
            title=p_data['title'],
            slug=p_data['slug'],
            description=p_data['description'],
            tag=p_data['tag'],
            benefit_metric=p_data['benefit_metric'],
            is_featured=p_data['is_featured'],
            order=p_data['order']
        )
        img_file = download_image(p_data['image_url'])
        if img_file:
            p.image.save(img_file.name, img_file, save=True)
        print(f"Created Program: {p.title}")

    # Success Stories
    SuccessStory.objects.all().delete()
    stories_data = [
        {
            'title': 'A Bridge to New Beginnings',
            'slug': 'bridge-to-new-beginnings',
            'tag': 'Housing Success',
            'summary': 'How AJ HOPE FOUNDATION helped Maria find a stable home and a new career in healthcare.',
            'image_url': 'https://images.unsplash.com/photo-1531417430048-8f35a099a531?w=800',
            'order': 1
        },
        {
            'title': 'Education: The Great Equalizer',
            'slug': 'education-great-equalizer',
            'tag': 'Education Success',
            'summary': 'From our youth literacy program to university graduate: Samuel story of resilience.',
            'image_url': 'https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?w=800',
            'order': 2
        }
    ]

    for s_data in stories_data:
        s = SuccessStory.objects.create(
            title=s_data['title'],
            slug=s_data['slug'],
            tag=s_data['tag'],
            summary=s_data['summary'],
            order=s_data['order']
        )
        img_file = download_image(s_data['image_url'])
        if img_file:
            s.image.save(img_file.name, img_file, save=True)
        print(f"Created SuccessStory: {s.title}")

    # News Stories
    NewsStory.objects.all().delete()
    news_data = [
        {
            'title': 'AJ HOPE FOUNDATION Expands to New Region',
            'slug': 'foundation-expands-new-region',
            'category': 'impact',
            'summary': 'Our mission continues to grow as we launch new community centers.',
            'content': 'In a significant milestone for our organization, we are thrilled to announce the opening of three new community centers.',
            'image_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
            'is_featured': True,
            'reading_time': 4
        },
        {
            'title': 'Volunteers Clean Up City Park',
            'slug': 'volunteers-cleanup-city-park',
            'category': 'community',
            'summary': 'Over 200 volunteers joined forces last Saturday for our annual cleanup.',
            'content': 'The city park was buzzing with activity as volunteers of all ages picked up litter and planted flowers.',
            'image_url': 'https://images.unsplash.com/photo-1542810634-71277d95dcbb?w=800',
            'is_featured': False,
            'reading_time': 3
        }
    ]

    for n_data in news_data:
        n = NewsStory.objects.create(
            title=n_data['title'],
            slug=n_data['slug'],
            category=n_data['category'],
            summary=n_data['summary'],
            content=n_data['content'],
            is_featured=n_data['is_featured'],
            reading_time=n_data['reading_time']
        )
        img_file = download_image(n_data['image_url'])
        if img_file:
            n.image.save(img_file.name, img_file, save=True)
        print(f"Created NewsStory: {n.title}")

    print("Programs, Success Stories, and News Stories seeding complete!")

if __name__ == '__main__':
    seed_extra()
