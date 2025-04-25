from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import AudioFile, UserProfile
from .forms import AudioFileForm, UserProfileForm
import datetime
import mimetypes
from django.http import HttpResponse, Http404
import os

def home(request):
    """Home page view - shows latest public audio uploads"""
    # Redirect authenticated users to dashboard/profile
    if request.user.is_authenticated:
        return redirect('profile')
    
    # User is not logged in - show only public files
    audio_files = AudioFile.objects.filter(
        is_public=True
    ).order_by('-upload_date')[:10]
    
    return render(request, 'audioapp/home.html', {'audio_files': audio_files})

@login_required
def upload_audio(request):
    """View for uploading audio files"""
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new AudioFile document
            audio = AudioFile(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                file=request.FILES['file'],
                upload_date=timezone.now(),
                user_id=request.user.id,
                artist=form.cleaned_data['artist'],
                album=form.cleaned_data['album'],
                genre=form.cleaned_data['genre'],
                tags=form.cleaned_data['tags'],
                is_public=form.cleaned_data.get('is_public', True),
                file_type=mimetypes.guess_type(request.FILES['file'].name)[0] or 'audio/mpeg'
            )
            audio.save()
            
            # Update user profile stats
            try:
                profile = UserProfile.objects.get(user_id=request.user.id)
                profile.total_uploads += 1
                profile.save()
            except UserProfile.DoesNotExist:
                # Create profile if it doesn't exist
                profile = UserProfile(
                    user_id=request.user.id,
                    total_uploads=1
                )
                profile.save()
                
            messages.success(request, 'Audio file uploaded successfully!')
            return redirect('home')
    else:
        form = AudioFileForm()
    
    return render(request, 'audioapp/upload.html', {'form': form})

@login_required
def my_audio_files(request):
    """View to display all audio files uploaded by the user"""
    audio_files = AudioFile.objects.filter(user_id=request.user.id).order_by('-upload_date')
    return render(request, 'audioapp/my_files.html', {'audio_files': audio_files})

@login_required
def profile(request):
    """View for user profile"""
    try:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user_id=request.user.id)
        user_profile.save()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Update user profile
            if form.cleaned_data.get('bio'):
                user_profile.bio = form.cleaned_data['bio']
            
            if form.cleaned_data.get('profile_picture'):
                user_profile.profile_picture = form.cleaned_data['profile_picture']
                
            user_profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(initial={
            'bio': user_profile.bio,
        })
    
    return render(request, 'audioapp/profile.html', {
        'form': form,
        'profile': user_profile
    })

def audio_detail(request, audio_id):
    """View for displaying details of a specific audio file"""
    try:
        audio = AudioFile.objects.get(id=audio_id)
        
        # Check if user has permission to view this file
        if not audio.is_public and (not request.user.is_authenticated or request.user.id != audio.user_id):
            messages.error(request, "You don't have permission to view this audio file.")
            return redirect('home')
            
        return render(request, 'audioapp/audio_detail.html', {'audio': audio})
    except AudioFile.DoesNotExist:
        messages.error(request, 'Audio file not found!')
        return redirect('home')

def about(request):
    """View for the About page"""
    return render(request, 'audioapp/about.html')

@login_required
def edit_audio(request, audio_id):
    """View for editing an existing audio file"""
    try:
        # Get the audio file
        audio = AudioFile.objects.get(id=audio_id)
        
        # Check if the user has permission to edit this file
        if request.user.id != audio.user_id:
            messages.error(request, "You don't have permission to edit this audio file.")
            return redirect('home')
        
        if request.method == 'POST':
            form = AudioFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Update fields
                audio.title = form.cleaned_data['title']
                audio.description = form.cleaned_data['description']
                audio.artist = form.cleaned_data['artist']
                audio.album = form.cleaned_data['album']
                audio.genre = form.cleaned_data['genre']
                audio.tags = form.cleaned_data['tags']
                audio.is_public = form.cleaned_data.get('is_public', True)
                
                # Check if a new file was uploaded
                if 'file' in request.FILES:
                    audio.file = request.FILES['file']
                    audio.file_type = mimetypes.guess_type(request.FILES['file'].name)[0] or 'audio/mpeg'
                
                audio.save()
                messages.success(request, 'Audio file updated successfully!')
                return redirect('audio_detail', audio_id=audio.id)
        else:
            # Pre-populate the form with existing data
            initial_data = {
                'title': audio.title,
                'description': audio.description,
                'artist': audio.artist,
                'album': audio.album,
                'genre': audio.genre,
                'tags': ', '.join(audio.tags) if audio.tags else '',
                'is_public': audio.is_public,
            }
            form = AudioFileForm(initial=initial_data)
        
        return render(request, 'audioapp/edit_audio.html', {
            'form': form,
            'audio': audio
        })
    except AudioFile.DoesNotExist:
        messages.error(request, 'Audio file not found!')
        return redirect('home')

@login_required
def delete_audio(request, audio_id):
    """View for deleting an audio file"""
    try:
        # Get the audio file
        audio = AudioFile.objects.get(id=audio_id)
        
        # Check if the user has permission to delete this file
        if request.user.id != audio.user_id:
            messages.error(request, "You don't have permission to delete this audio file.")
            return redirect('home')
        
        if request.method == 'POST':
            # Update user profile stats
            try:
                profile = UserProfile.objects.get(user_id=request.user.id)
                if profile.total_uploads > 0:
                    profile.total_uploads -= 1
                profile.save()
            except UserProfile.DoesNotExist:
                pass
            
            # Delete the audio file
            audio_title = audio.title
            audio.delete()
            messages.success(request, f'"{audio_title}" has been deleted successfully.')
            return redirect('my_audio_files')
        
        return render(request, 'audioapp/delete_audio.html', {'audio': audio})
    except AudioFile.DoesNotExist:
        messages.error(request, 'Audio file not found!')
        return redirect('home')

def serve_audio(request, audio_id):
    """Serve audio file from GridFS"""
    try:
        audio = AudioFile.objects.get(id=audio_id)
        
        # Check if user has permission to access this file
        if not audio.is_public and (not request.user.is_authenticated or request.user.id != audio.user_id):
            return HttpResponse(status=403)  # Forbidden
        
        # Increments listens count if needed
        # This could be moved to a separate API endpoint if you want to track only genuine listens
        try:
            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user_id=request.user.id)
                profile.total_listens += 1
                profile.save()
        except UserProfile.DoesNotExist:
            pass
        
        # Get file from GridFS
        grid_file = audio.file
        content_type = audio.file_type if audio.file_type else 'audio/mpeg'
        
        # Set response headers
        response = HttpResponse(grid_file.read(), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{audio.get_filename()}"'
        response['Content-Length'] = grid_file.length
        
        return response
    except AudioFile.DoesNotExist:
        raise Http404("Audio file not found")

@login_required
def update_profile(request):
    """View for updating user profile"""
    # Get the user's profile or create it if it doesn't exist
    try:
        profile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user_id=request.user.id)
        profile.save()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Update profile fields
            if 'bio' in form.cleaned_data:
                profile.bio = form.cleaned_data['bio']
            
            if 'profile_picture' in form.cleaned_data and form.cleaned_data['profile_picture']:
                # Xóa ảnh cũ nếu cần
                if profile.profile_picture:
                    try:
                        profile.profile_picture.delete()
                    except:
                        pass
                # Lưu ảnh mới
                profile.profile_picture = form.cleaned_data['profile_picture']
                
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            # Thêm timestamp vào URL redirect để tránh cache
            timestamp = int(timezone.now().timestamp())
            return redirect(f'/profile/?t={timestamp}')
    else:
        form = UserProfileForm(initial={
            'bio': profile.bio,
        })
    
    return render(request, 'audioapp/update_profile.html', {'form': form, 'profile': profile})

def serve_profile_image(request, profile_id):
    """Serve profile image from GridFS"""
    try:
        profile = UserProfile.objects.get(id=profile_id)
        
        # Check if profile image exists
        if not profile.profile_picture:
            raise Http404("Profile image not found")
        
        # Get file from GridFS
        grid_file = profile.profile_picture
        content_type = 'image/jpeg'  # Default to JPEG
        
        # Try to determine content type from filename
        if grid_file.name:
            filename = grid_file.name.lower()
            if filename.endswith('.png'):
                content_type = 'image/png'
            elif filename.endswith('.gif'):
                content_type = 'image/gif'
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                content_type = 'image/jpeg'
        
        # Set response headers
        response = HttpResponse(grid_file.read(), content_type=content_type)
        
        # Check if grid_file has a name before trying to use it
        if grid_file.name:
            filename = os.path.basename(grid_file.name)
            response['Content-Disposition'] = f'inline; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="profile_{profile_id}.jpg"'
            
        if hasattr(grid_file, 'length'):
            response['Content-Length'] = grid_file.length
        
        # Add cache-busting headers to prevent browser caching
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
    except UserProfile.DoesNotExist:
        raise Http404("Profile not found")
