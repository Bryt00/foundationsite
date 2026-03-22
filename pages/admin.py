from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from pages.models import (
    NewsStory, TeamMember, TimelineEvent, CoreValue,
    ProgramCategory, Program, ProgramStat,
    ImpactStat, FundAllocation, SuccessStory,
    Volunteer, ContactMessage, GalleryImage,
    Event, FAQ, HeroSlide, SiteSettings,
    ProgramMedia, EventMedia, RegionalOffice, RegionalOfficePhone,
    DonationMethod
)
from django.shortcuts import redirect
from django.urls import reverse

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ('__str__', 'contact_email', 'contact_phone')

    fieldsets = (
        ('Contact Information', {
            'fields': ('contact_email', 'support_email', 'contact_phone', 'headquarters_address', 'office_hours')
        }),
        ('Donation Methods', {
            'fields': ('zelle_email', 'cashapp_tag', 'check_payable_to')
        }),
        ('Mission & Vision', {
            'fields': ('mission_statement', 'vision_statement')
        }),
        ('Home Page Mission Section', {
            'fields': ('home_mission_title', 'home_mission_subtitle', 'home_mission_image', 'about_mission_image')
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'linkedin_url')
        }),
        ('Trust & Transparency', {
            'fields': ('charity_navigator_url', 'guidestar_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the settings to ensure singleton exists
        return False

    def changelist_view(self, request, extra_context=None):
        """
        Redirect the list view to the only instance's change view,
        or to the add view if no instance exists.
        """
        obj = SiteSettings.objects.first()
        if obj:
            return redirect(reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk,)))
        else:
            return redirect(reverse(f'admin:{SiteSettings._meta.app_label}_{SiteSettings._meta.model_name}_add'))

@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

class EventMediaInline(TabularInline):
    model = EventMedia
    extra = 1

@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "date", "location", "is_major", "is_completed")
    list_filter = ("is_major", "is_completed", "date")
    list_editable = ("is_completed",)
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventMediaInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'description', 'location', 'date', 'is_major', 'registration_link')
        }),
        ('Past Event', {
            'fields': ('is_completed', 'completion_date'),
            'description': 'Mark this event as completed to move it to the \'Past Events\' section.'
        }),
    )

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ("title", "category", "media_type", "order", "date_added")
    list_filter = ("category",)
    search_fields = ("title", "caption")
    ordering = ("order", "-date_added")

    @admin.display(description="Type")
    def media_type(self, obj):
        if obj.video_url or obj.video_file:
            return "Video"
        return "Image"

@admin.register(Volunteer)
class VolunteerAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'interest', 'date_submitted')
    list_filter = ('interest', 'date_submitted')

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'subject', 'date_submitted', 'is_read')
    list_filter = ('is_read', 'date_submitted')

@admin.register(NewsStory)
class NewsStoryAdmin(ModelAdmin):
    list_display = ('title', 'category', 'date_published', 'is_featured')
    list_filter = ('category', 'is_featured', 'date_published')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)

@admin.register(TimelineEvent)
class TimelineEventAdmin(ModelAdmin):
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)

@admin.register(CoreValue)
class CoreValueAdmin(ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(ProgramCategory)
class ProgramCategoryAdmin(ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

class ProgramMediaInline(TabularInline):
    model = ProgramMedia
    extra = 1

@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_completed", "order")
    list_filter = ("category", "is_featured", "is_completed")
    list_editable = ('is_featured', 'is_completed', 'order')
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProgramMediaInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'image', 'description', 'tag', 'benefit_metric', 'is_featured', 'order')
        }),
        ('Past Program', {
            'fields': ('is_completed', 'completion_date'),
            'description': 'Mark this program as completed to move it to the \'Past Programs\' section.'
        }),
    )

@admin.register(ProgramStat)
class ProgramStatAdmin(ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('order',)

@admin.register(ImpactStat)
class ImpactStatAdmin(ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('order',)

@admin.register(FundAllocation)
class FundAllocationAdmin(ModelAdmin):
    list_display = ('label', 'percentage', 'order')
    list_editable = ('order',)

@admin.register(SuccessStory)
class SuccessStoryAdmin(ModelAdmin):
    list_display = ('title', 'tag', 'order')
    list_editable = ('order',)

class RegionalOfficePhoneInline(TabularInline):
    model = RegionalOfficePhone
    extra = 1

@admin.register(RegionalOffice)
class RegionalOfficeAdmin(ModelAdmin):
    list_display = ('name', 'region', 'order')
    list_editable = ('order',)
    inlines = [RegionalOfficePhoneInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'region', 'description', 'order')
        }),
        ('Contact Information', {
            'fields': ('address', 'email')
        }),
    )

@admin.register(DonationMethod)
class DonationMethodAdmin(ModelAdmin):
    list_display = ('name', 'value', 'order', 'is_active')
    list_editable = ('order', 'is_active')
