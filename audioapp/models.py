from mongoengine import Document, EmbeddedDocument, fields
from django.contrib.auth.models import User
import os
from django.urls import reverse

class AudioFile(Document):
    """
    Model to store audio files metadata in MongoDB.
    The actual file will be stored using MongoEngine's FileField, which uses GridFS.
    """
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField(max_length=1000)
    file = fields.FileField(required=True)
    upload_date = fields.DateTimeField(default=None)
    duration = fields.FloatField(default=0.0)  # Duration in seconds
    
    # Link to Django User model (which is stored in the SQL database)
    user_id = fields.IntField(required=True)
    
    # File visibility - public or private
    is_public = fields.BooleanField(default=True)
    
    # Optional metadata fields
    artist = fields.StringField(max_length=255)
    album = fields.StringField(max_length=255)
    genre = fields.StringField(max_length=100)
    tags = fields.ListField(fields.StringField(max_length=50))
    
    # File details
    file_size = fields.IntField()  # Size in bytes
    file_type = fields.StringField(max_length=50)  # MIME type
    
    meta = {
        'collection': 'audio_files',
        'indexes': [
            'title',
            'user_id',
            'upload_date',
            'genre',
            'tags',
            'is_public'
        ]
    }
    
    def __str__(self):
        return self.title
    
    def get_filename(self):
        if self.file and hasattr(self.file, 'name') and self.file.name:
            return os.path.basename(self.file.name)
        return f"audio_{self.id}.mp3"  # Default filename based on ID
    
    def get_file_url(self):
        """
        Returns a proper URL to access the audio file through Django
        """
        return reverse('serve_audio', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        # Automatically set file_size and file_type when saving
        if self.file and not self.file_size:
            self.file_size = self.file.length
        super().save(*args, **kwargs)

class UserProfile(Document):
    """
    Extended user profile stored in MongoDB.
    Links to Django's built-in User model by user_id.
    """
    user_id = fields.IntField(required=True, unique=True)
    bio = fields.StringField(max_length=1000)
    profile_picture = fields.ImageField()
    preferences = fields.DictField()  # For storing user preferences
    
    # Stats
    total_uploads = fields.IntField(default=0)
    total_listens = fields.IntField(default=0)
    total_deepfakes = fields.IntField(default=0)
    total_authentic = fields.IntField(default=0)
    
    meta = {
        'collection': 'user_profiles',
        'indexes': ['user_id']
    }
    
    def __str__(self):
        return f"Profile for user {self.user_id}"
    
    def get_profile_picture_url(self):
        """Returns the URL for the profile picture or None if no picture exists"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return None
