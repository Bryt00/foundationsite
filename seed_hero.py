import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churchsite.settings')
django.setup()

from pages.models import HeroSlide

def seed_hero():
    print("Seeding Hero Carousel data...")
    HeroSlide.objects.all().delete()

    slides = [
        {
            'title': 'Faith in Action.<br><span class="text-accent italic font-light">Transforming Communities.</span>',
            'subtitle': 'We are dedicated to bridging gaps, alleviating poverty, and fostering hope through AJ HOPE FOUNDATION programs.',
            'image_path': 'media/hero/hero1.jpg',
            'button_text': 'Get Involved',
            'button_link': '/join/',
            'order': 1
        },
        {
            'title': 'Empowering the <br><span class="text-accent italic font-light">Next Generation.</span>',
            'subtitle': 'Our mentorship and education programs provide children with the tools they need to build a brighter future.',
            'image_path': 'media/hero/hero2.jpg',
            'button_text': 'Our Programs',
            'button_link': '/programs/',
            'order': 2
        },
        {
            'title': 'Crisis Relief & <br><span class="text-accent italic font-light">Global Support.</span>',
            'subtitle': 'Providing immediate humanitarian aid and long-term recovery support to communities affected by natural disasters.',
            'image_path': 'media/hero/hero3.jpg',
            'button_text': 'Learn More',
            'button_link': '/impact/',
            'order': 3
        }
    ]

    for slide in slides:
        h = HeroSlide.objects.create(
            title=slide['title'],
            subtitle=slide['subtitle'],
            button_text=slide['button_text'],
            button_link=slide['button_link'],
            order=slide['order']
        )
        # Manually assign the image path relative to MEDIA_ROOT
        h.image = f"hero/{os.path.basename(slide['image_path'])}"
        h.save()
        print(f"Created Slide: {slide['title']}")

    print("Hero Carousel seeding complete!")

if __name__ == '__main__':
    seed_hero()
