from django.db import models

class Profile(models.Model):
    # data attributes of a Profile:
    fname = models.TextField(blank=False)
    lname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    
    def get_status_messages(self):
        '''Return all of the status messages about this profile.'''
        statusmessage = StatusMessage.objects.filter(profile=self)
        return statusmessage

class StatusMessage(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all the images associated with this StatusMessage.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the Image object.'''
        return f'Image for StatusMessage {self.status_message.id} uploaded at {self.timestamp}'