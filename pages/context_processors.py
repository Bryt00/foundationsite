from pages.models import SiteSettings

def site_settings(request):
    """
    Makes the SiteSettings singleton available globally in templates as 'site_settings'.
    """
    # Get the first settings object, or create one with defaults if it doesn't exist
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    
    return {
        'site_settings': settings
    }
