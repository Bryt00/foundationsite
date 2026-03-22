from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import (
    NewsStory, TeamMember, TimelineEvent, CoreValue, 
    ProgramCategory, Program, ProgramStat,
    ImpactStat, FundAllocation, SuccessStory,
    GalleryImage, Event, FAQ, HeroSlide,
    RegionalOffice, DonationMethod
)

def gallery(request):
    images = GalleryImage.objects.all()
    categories = GalleryImage.CATEGORY_CHOICES
    return render(request, 'pages/gallery.html', {
        'images': images,
        'categories': categories
    })

def landing_page(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    featured_news = NewsStory.objects.filter(is_featured=True)[:3]
    latest_programs = Program.objects.filter(is_featured=True)[:3]
    if not latest_programs:
        latest_programs = Program.objects.all()[:3]
    
    impact_stats = ImpactStat.objects.all()[:3]
    events = Event.objects.all()[:3]
    faqs = FAQ.objects.all()[:3]
    team = TeamMember.objects.all()[:4]
    stories = SuccessStory.objects.all()[:2]

    return render(request, 'pages/landing.html', {
        'hero_slides': hero_slides,
        'featured_news': featured_news,
        'latest_programs': latest_programs,
        'impact_stats': impact_stats,
        'events': events,
        'faqs': faqs,
        'team': team,
        'stories': stories
    })

def about(request):
    team = TeamMember.objects.all()
    timeline = TimelineEvent.objects.all()
    values = CoreValue.objects.all()
    return render(request, 'pages/about.html', {
        'team': team,
        'timeline': timeline,
        'values': values
    })

def impact(request):
    stats = ImpactStat.objects.all()
    allocations = FundAllocation.objects.all()
    stories = SuccessStory.objects.all()
    return render(request, 'pages/impact.html', {
        'stats': stats,
        'allocations': allocations,
        'stories': stories
    })

def programs(request):
    categories = ProgramCategory.objects.prefetch_related('programs').all()
    stats = ProgramStat.objects.all()
    past_programs = Program.objects.filter(is_completed=True).order_by('-completion_date')
    return render(request, 'pages/programs.html', {
        'categories': categories,
        'stats': stats,
        'past_programs': past_programs,
    })

def news(request):
    featured_story = NewsStory.objects.filter(is_featured=True).first()
    stories_list = NewsStory.objects.filter(is_featured=False)
    
    paginator = Paginator(stories_list, 2) # Show 2 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/news.html', {
        'featured_story': featured_story,
        'page_obj': page_obj,
        'other_stories_preview': stories_list[:2] # For the sidebar/header previews
    })

from django.contrib import messages
from .forms import VolunteerForm, ContactForm

def join(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your interest! We will contact you soon.')
            return render(request, 'pages/join.html', {'form': VolunteerForm(), 'success': True})
    else:
        form = VolunteerForm()
    donation_methods = DonationMethod.objects.filter(is_active=True)
    return render(request, 'pages/join.html', {
        'form': form,
        'donation_methods': donation_methods
    })

def contact(request):
    regional_offices = RegionalOffice.objects.prefetch_related('phones').all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you shortly.')
            return render(request, 'pages/contact.html', {
                'form': ContactForm(), 
                'success': True,
                'regional_offices': regional_offices
            })
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {
        'form': form,
        'regional_offices': regional_offices
    })

def story_detail(request, slug):
    story = get_object_or_404(NewsStory, slug=slug)
    # Get relevant/recent stories for sidebar
    recent_stories = NewsStory.objects.exclude(id=story.id)[:3]
    
    # Next/Prev navigation
    next_story = NewsStory.objects.filter(date_published__gt=story.date_published).order_by('date_published').first()
    prev_story = NewsStory.objects.filter(date_published__lt=story.date_published).order_by('-date_published').first()
    
    return render(request, 'pages/story_detail.html', {
        'story': story,
        'recent_stories': recent_stories,
        'next_story': next_story,
        'prev_story': prev_story,
    })

def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    # Get other programs in the same category
    related_programs = Program.objects.filter(category=program.category).exclude(id=program.id)[:3]
    return render(request, 'pages/program_detail.html', {
        'program': program,
        'related_programs': related_programs
    })

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    # Get upcoming events
    upcoming_events = Event.objects.filter(date__gt=timezone.now()).exclude(id=event.id)[:3]
    return render(request, 'pages/event_detail.html', {
        'event': event,
        'upcoming_events': upcoming_events
    })

def success_story_detail(request, slug):
    story = get_object_or_404(SuccessStory, slug=slug)
    # Get other success stories
    other_stories = SuccessStory.objects.exclude(id=story.id)[:3]
    return render(request, 'pages/success_story_detail.html', {
        'story': story,
        'other_stories': other_stories
    })
