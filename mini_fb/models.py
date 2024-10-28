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
    
    def get_friends(self):
        '''Return a list of friend's profiles associated with this profile.'''
        profile1_friends = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        
        profile2_friends = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        all_friends = Profile.objects.filter(id__in=profile1_friends.union(profile2_friends))

        return list(all_friends)
    
    def add_friend(self, other):
        '''Add a Friend relation for self and other, if it doesn't already exist.'''
        if self == other:
            return
        
        friendship_exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        if not friendship_exists:
            Friend.objects.create(profile1=self, profile2=other)
            
    def get_friend_suggestions(self):
        '''Return a list of possible friends for this profile.'''
        friends = self.get_friends()
        suggestions = Profile.objects.exclude(id__in=[friend.pk for friend in friends]).exclude(id=self.pk)

        return suggestions
    
    def get_news_feed(self):
        '''Return a list of all StatusMessages for the profile and its friends, sorted by most recent.'''
        friends = self.get_friends()
        profile_ids = [self.pk] + [friend.pk for friend in friends]

        news_feed = StatusMessage.objects.filter(profile_id__in=profile_ids).order_by('-timestamp')

        return news_feed


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
        return f'Image for StatusMessage {self.status_message.id} uploaded at {self.timestamp}' # type: ignore
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of the relationship between friends.'''
        return f'{self.profile1.fname} {self.profile1.lname} & {self.profile2.fname} {self.profile2.lname}'