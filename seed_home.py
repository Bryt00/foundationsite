import os
import django
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
from urllib.parse import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churchsite.settings')
django.setup()

from pages.models import Event, FAQ, TeamMember

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

def seed_home():
    print("Seeding Home Page, Events, and Team data...")

    # Events
    Event.objects.all().delete()
    events_data = [
        {
            'title': 'Global Peace Summit 2025',
            'slug': 'global-peace-summit-2025',
            'date': timezone.now() + timedelta(days=20, hours=10),
            'location': 'Grand Hall, Geneva',
            'description': 'A gathering of global leaders and activists to discuss sustainable peace and community resilience.',
            'image_url': 'https://images.unsplash.com/photo-1528605248644-14dd04cb21c7?w=800',
            'is_major': True,
            'registration_link': 'https://example.com/register/peace-summit'
        },
        {
            'title': 'Community Health Fair',
            'slug': 'community-health-fair',
            'date': timezone.now() + timedelta(days=45, hours=9),
            'location': 'Nairobi Community Center',
            'description': 'Providing free health screenings, vaccinations, and wellness workshops for local residents.',
            'image_url': 'https://images.unsplash.com/photo-1576091160550-217359f42f8c?w=800',
            'is_major': False,
            'registration_link': 'https://example.com/register/health-fair'
        },
        {
            'title': 'Youth Mentorship Workshop',
            'slug': 'youth-mentorship-workshop',
            'date': timezone.now() + timedelta(days=60, hours=14),
            'location': 'Online (Global)',
            'description': 'Connecting young leaders with experienced professionals for a weekend of intensive skills training.',
            'image_url': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800',
            'is_major': False,
            'registration_link': 'https://example.com/register/youth-mentorship'
        }
    ]

    for data in events_data:
        image_url = data.pop('image_url')
        e = Event.objects.create(**data)
        img_file = download_image(image_url)
        if img_file:
            e.image.save(img_file.name, img_file, save=True)
        print(f"Created Event: {e.title}")

    # Team Members
    TeamMember.objects.all().delete()
    team_data = [
        {
            'name': 'Dr. Sarah Johnson',
            'role': 'Executive Director',
            'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800',
            'bio': 'Sarah has over 15 years of experience in international development and non-profit management.',
            'order': 1
        },
        {
            'name': 'James Mwangi',
            'role': 'Director of Programs',
            'image_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=800',
            'bio': 'James leads our on-the-ground initiatives with a focus on sustainable community impact.',
            'order': 2
        },
        {
            'name': 'Elena Rodriguez',
            'role': 'Community Foundation Lead',
            'image_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=800',
            'bio': 'Elena is dedicated to fostering strong relationships between our organization and the local community.',
            'order': 3
        }
    ]

    for t_data in team_data:
        t = TeamMember.objects.create(
            name=t_data['name'],
            role=t_data['role'],
            bio=t_data['bio'],
            order=t_data['order']
        )
        img_file = download_image(t_data['image_url'])
        if img_file:
            t.image.save(img_file.name, img_file, save=True)
        print(f"Created Team Member: {t.name}")

    # FAQs
    FAQ.objects.all().delete()
    faqs_data = [
        {
            'question': 'How can I donate if I am outside the US?',
            'answer': 'We accept international donations via wire transfer, major credit cards, and PayPal.',
            'order': 1
        },
        {
            'question': 'Can I volunteer for a specific program?',
            'answer': 'Absolutely! Our application form allows you to select your interests (Education, Health, Logistics, etc.).',
            'order': 2
        },
        {
            'question': 'Are your financial reports public?',
            'answer': 'Yes. We pride ourselves on radical transparency. You can download our annual impact reports and audited financial statements.',
            'order': 3
        }
    ]

    for data in faqs_data:
        FAQ.objects.create(**data)
        print(f"Created FAQ: {data['question']}")

    print("Home Page seeding complete!")

if __name__ == '__main__':
    seed_home()
