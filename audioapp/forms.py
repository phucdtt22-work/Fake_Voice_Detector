from django import forms
from .models import AudioFile, UserProfile

class AudioFileForm(forms.Form):
    """
    Form for uploading audio files
    """
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField()
    artist = forms.CharField(max_length=255, required=False)
    album = forms.CharField(max_length=255, required=False)
    genre = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=255, required=False, 
                           help_text="Enter tags separated by commas")
    is_public = forms.BooleanField(
        label="Make this file public",
        required=False,
        initial=True,
        help_text="If checked, this file will be visible to everyone. If unchecked, only you can see it."
    )
    
    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')
        if tags_string:
            # Split tags by comma and strip whitespace
            tags = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
            return tags
        return []

class UserProfileForm(forms.Form):
    """
    Form for user profile information
    """
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)