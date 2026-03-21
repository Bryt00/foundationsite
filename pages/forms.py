from django import forms
from .models import Volunteer, ContactMessage


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'email', 'phone', 'interest', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all',
                'placeholder': '(555) 000-0000'
            }),
            'interest': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-100 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-brand-500 outline-none transition-all',
                'rows': 4,
                'placeholder': 'How would you like to help?'
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'peer w-full bg-transparent border-b-2 border-gray-200 py-3 outline-none focus:border-brand-600 transition-colors',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'peer w-full bg-transparent border-b-2 border-gray-200 py-3 outline-none focus:border-brand-600 transition-colors',
                'placeholder': ' '
            }),
            'subject': forms.TextInput(attrs={
                'class': 'peer w-full bg-transparent border-b-2 border-gray-200 py-3 outline-none focus:border-brand-600 transition-colors',
                'placeholder': ' '
            }),
            'message': forms.Textarea(attrs={
                'class': 'peer w-full bg-transparent border-b-2 border-gray-200 py-3 outline-none focus:border-brand-600 transition-colors',
                'rows': 4,
                'placeholder': ' '
            }),
        }
