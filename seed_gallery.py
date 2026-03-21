import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churchsite.settings')
django.setup()

from pages.models import GalleryImage

def seed_gallery():
    print("Seeding Gallery data...")
    GalleryImage.objects.all().delete()

    images = [
        {
            'title': 'Community Food Drive',
            'caption': 'Our weekly local food distribution program in action.',
            'category': 'community',
            'image_path': 'gallery/comm1.jpg',
            'order': 1
        },
        {
            'title': 'Neighborhood Cleanup',
            'caption': 'Volunteers working together to beautify our community parks.',
            'category': 'community',
            'image_path': 'gallery/comm2.jpg',
            'order': 2
        },
        {
            'title': 'Youth Literacy Program',
            'caption': 'Students engaged in our after-school reading and mentorship initiative.',
            'category': 'programs',
            'image_path': 'gallery/prog1.jpg',
            'order': 3
        },
        {
            'title': 'Vocational Training',
            'caption': 'Adults learning sustainable job skills in our workshop.',
            'category': 'programs',
            'image_path': 'gallery/prog2.jpg',
            'order': 4
        },
        {
            'title': 'Annual Charity Gala',
            'caption': 'Celebrating our progress and partners at the year-end gala.',
            'category': 'events',
            'image_path': 'gallery/ev1.jpg',
            'order': 5
        },
        {
            'title': 'Healthcare Awareness Seminar',
            'caption': 'Local doctors providing essential health information to the community.',
            'category': 'events',
            'image_path': 'gallery/ev2.jpg',
            'order': 6
        },
        {
            'title': 'Our Main Community Center',
            'caption': 'The heart of our operations, serving hundreds daily.',
            'category': 'facility',
            'image_path': 'gallery/fac1.jpg',
            'order': 7
        },
        {
            'title': 'New Vocational Wing',
            'caption': 'A sneak peek at our newly expanded educational facilities.',
            'category': 'facility',
            'image_path': 'gallery/fac2.jpg',
            'order': 8
        }
    ]

    for data in images:
        GalleryImage.objects.create(
            title=data['title'],
            caption=data['caption'],
            category=data['category'],
            image=data['image_path'], # Relative to MEDIA_ROOT
            order=data['order']
        )
        print(f"Created GalleryImage: {data['title']}")

    print("Gallery seeding complete!")

if __name__ == '__main__':
    seed_gallery()
