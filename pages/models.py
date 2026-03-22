from django.db import models

class NewsStory(models.Model):
    CATEGORY_CHOICES = [
        ('impact', 'Impact'),
        ('event', 'Event'),
        ('community', 'Community'),
        ('relief', 'Relief'),
        ('press', 'Press'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Used for the URL of the story")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='community')
    summary = models.TextField(help_text="A short teaser for the card view")
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    date_published = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")

    class Meta:
        verbose_name_plural = "News Stories"
        ordering = ['-date_published']

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class TimelineEvent(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"

class CoreValue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.TextField(help_text="Paste SVG path or shorthand for the icon")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class ProgramCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.TextField(help_text="SVG path for the category icon")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Program Categories"
        ordering = ['order']

    def __str__(self):
        return self.title

class Program(models.Model):
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True, help_text="Used for the URL of the program")
    description = models.TextField()
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    tag = models.CharField(max_length=50, blank=True, help_text="e.g. Weekly, 24/7 Access")
    benefit_metric = models.CharField(max_length=100, blank=True, help_text="e.g. 1,000+ families/week")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # New fields for past/completed content
    is_completed = models.BooleanField(default=False, help_text="Check if this is a past/completed program")
    completion_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class ProgramMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='programs/gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube, Vimeo, etc.")
    video_file = models.FileField(upload_to='programs/videos/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Program Media"

    def __str__(self):
        return f"{self.media_type.title()} for {self.program.title}"

class ProgramStat(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"

class ImpactStat(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    color_choice = models.CharField(max_length=20, choices=[('brand', 'Brand (Teal)'), ('accent', 'Accent (Amber)')], default='brand')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"

class FundAllocation(models.Model):
    label = models.CharField(max_length=100)
    percentage = models.IntegerField()
    color_hex = models.CharField(max_length=7, default="#0d9488", help_text="Tailwind brand-600 is #0d9488")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.percentage}%)"

class SuccessStory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True, help_text="Used for the URL of the story")
    tag = models.CharField(max_length=50, default="Success Story")
    summary = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Success Stories"
        ordering = ['order']

    def __str__(self):
        return self.title

class Volunteer(models.Model):
    INTEREST_CHOICES = [
        ('community', 'Community Foundation'),
        ('education', 'Education & Tutoring'),
        ('relief', 'Crisis Relief'),
        ('admin', 'Administrative Support'),
        ('event', 'Events & Hospitality'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    message = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_interest_display()})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('community', 'Community'),
        ('programs', 'Programs'),
        ('events', 'Events'),
        ('facility', 'Our Facility'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, help_text="Required for images, or as thumbnail for videos")
    video_url = models.URLField(blank=True, null=True, help_text="Supporting YouTube, Vimeo, etc.")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, help_text="Direct video upload")
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def is_video(self):
        return bool(self.video_url or self.video_file)

    class Meta:
        ordering = ['order', '-date_added']
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True, help_text="Used for the URL of the event")
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_major = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True)

    # Past / completed event support
    is_completed = models.BooleanField(default=False, help_text="Check if this is a past/completed event")
    completion_date = models.DateField(blank=True, null=True, help_text="Date the event took place (for past events)")

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

class EventMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='events/gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube, Vimeo, etc.")
    video_file = models.FileField(upload_to='events/videos/', blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Event Media"

    def __str__(self):
        return f"{self.media_type.title()} for {self.event.title}"

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

class HeroSlide(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero/')
    button_text = models.CharField(max_length=50, default='Learn More')
    button_link = models.CharField(max_length=200, default='#')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    contact_email = models.EmailField(default='contact@ajhopefoundation.org')
    support_email = models.EmailField(default='help@ajhopefoundation.org')
    contact_phone = models.CharField(max_length=20, default='+1 (888) 123-4567')
    
    # Donation Methods
    zelle_email = models.EmailField(default='ajhopefoundation@gmail.com')
    cashapp_tag = models.CharField(max_length=50, default='$ajhopefoundationgh')
    check_payable_to = models.CharField(max_length=100, default='AJ Hope Foundation')
    
    # Social Links
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    # New Dynamic Content Fields
    headquarters_address = models.TextField(default='123 AJ HOPE Avenue, Faith Plaza, Springfield, IL 62704')
    office_hours = models.CharField(max_length=100, default='Mon-Fri, 9am - 5pm CST', blank=True, null=True)
    mission_statement = models.TextField(default="To demonstrate God's love through practical service, sustainable development, and unwavering community support.")
    vision_statement = models.TextField(default="A city where no one is forgotten, and every person has the opportunity to fulfill their potential.")
    
    # Home Page Mission Section (Dynamic)
    home_mission_title = models.CharField(
        max_length=255, 
        default='Driven by Compassion, <br><span class="text-accent">Guided by Faith.</span>',
        help_text="Supports HTML for styling (e.g. &lt;br&gt;, &lt;span&gt;)"
    )
    home_mission_subtitle = models.TextField(
        default='Founded on the principles of unconditional support, AJ HOPE FOUNDATION operates at the intersection of practical relief and spiritual empowerment.'
    )
    home_mission_image = models.ImageField(
        upload_to='site_settings/', 
        blank=True, 
        null=True,
        help_text="If empty, a default Unsplash image will be used."
    )

    charity_navigator_url = models.URLField(blank=True, null=True)
    guidestar_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Global Site Settings"

    def save(self, *args, **kwargs):
        # Singleton pattern: only one instance allowed
        if not self.pk and SiteSettings.objects.exists():
            return
        super().save(*args, **kwargs)

class RegionalOffice(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, help_text="e.g. North America, East Africa")
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, help_text="Short description of the office focus")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.region})"

class RegionalOfficePhone(models.Model):
    office = models.ForeignKey(RegionalOffice, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)
    label = models.CharField(max_length=50, blank=True, help_text="e.g. Main, Support, SMS")

    def __str__(self):
        return f"{self.phone_number} ({self.label})" if self.label else self.phone_number

class DonationMethod(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. PayPal, Venmo, Zelle")
    value = models.CharField(max_length=200, help_text="The email, tag, or account number")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
