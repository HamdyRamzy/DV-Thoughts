from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import DecimalField
from django.utils.text import Truncator
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save, post_delete, pre_delete
from PIL import Image
from notifications.models import Notification
from datetime import datetime, date





class Badge(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50, unique=True)
    description = models.CharField(null=True, blank=True, max_length=150)
    medal = models.ImageField(null=True, blank=True, upload_to='badges/%y/%m/%d', default='static/images/trophy.png')
    def __str__(self):
        return self.name

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='author')
    badge = models.ManyToManyField(Badge, default=None, blank=True, related_name='user_badges')
    bio = models.CharField(max_length=300, blank=True, null=True)
    picture = models.ImageField(null=True, blank=True, upload_to='photos/%y/%m/%d')
    uploaded_date = models.DateTimeField(null=True)
    work = models.CharField(max_length=300, blank=True, null=True)
    education = models.CharField(max_length=300, blank=True, null=True)
    skills = models.CharField(max_length=300, blank=True, null=True)
    facebook = models.URLField(max_length = 200, blank=True, null=True)
    github = models.URLField(max_length = 200, blank=True, null=True)
    progress = models.PositiveIntegerField(default=0, null=True)

    
    @property
    def get_progress(self):

        if self.picture:
            self.progress = self.progress+25

        else:
            self.picture = self.progress-25

        if self.bio:
            self.progress = self.progress+25

        else:
            self.bio = self.progress-25    

        if self.work:
            self.progress = self.progress+25

        else:
            self.work = self.progress-25    
        
        if self.education:
            self.progress = self.progress+25

        else:
            self.education = self.progress-25        


        return self.progress
         


    @property
    def get_badge(self):
        medal_20_topic = Badge.objects.filter(name='20 topics badge').first()
        medal_one_year = Badge.objects.filter(name='one year badge').first()
        medal_complete_fields = Badge.objects.filter(name='Autobiographer badge').first()

        
        if self.user.topics.count() >= 20:
            self.badge.add(medal_20_topic)

        else:
            self.badge.remove( medal_20_topic)
            

        if self.user.date_joined.year < datetime.now().year:
            self.badge.add(medal_one_year)

        else:
            self.badge.remove(medal_one_year)    


        if self.bio and self.picture and self.work and self.education:
            self.badge.add(medal_complete_fields)

        else:
            self.badge.remove(medal_complete_fields)    
   
                
        return self.badge 

    

    def __str__(self):
        return '%s' %(self.user)



def create_author(sender, **kwargs):
    if kwargs['created']:
        author = Author.objects.create(user=kwargs['instance'])
post_save.connect(create_author, sender=User)            







class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150)
    picture = models.ImageField(null=True, blank=True, upload_to='boards/%y/%m/%d')

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()    

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_date').first()   

        

# Topic Model contains (Topic subject, created_by, created_date)
class Topic(models.Model):
    subject = models.CharField(max_length=300)
    content = RichTextUploadingField()
    topic_picture = models.ImageField(null=True, upload_to='topic_picture/%y/%m/%d')
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    liked =  models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    created_date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0) 
    tags = TaggableManager()
    time = models.PositiveIntegerField(null=True)
    is_blocked = models.BooleanField(default=False)



    @property
    def num_likes(self):
        return self.liked.all().count()


    def __str__(self):
        return self.subject


LIKES_CHOICES = {
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
}
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKES_CHOICES, max_length=10, default='Like')

    

    def add_like_notification(self, sender, topic):
        notify = Notification.objects.create(topic=topic, sender=sender, user=topic.created_by, notification_type=1)

    
    def delete_like_notification(self, sender, topic):
        notify = Notification.objects.filter(topic=topic, sender=sender, user=topic.created_by, notification_type=1)
        notify.delete()

    
    def __str__(self):
        return str(self.value) 


        



REPORT_TYPES = {
    ('Nudity', 'Nudity'),
    ('Violence', 'Violence'),
    ('Harassment', 'Harassment'),
    ('Suicide or self-injury', 'Suicide or self-injury'),
    ('False information', 'False information'),
    ('Spam', 'Spam'),
    ('Terrorism', 'Terrorism'),
    ('Something else', 'Something else'),
}



class Report_topic(models.Model):
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="report_topic", blank=True, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_to_user")
	report_type = models.CharField(choices=REPORT_TYPES, max_length=100)
	description = models.TextField(max_length=400)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)



class Report_user(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_sender")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_user")
	report_type = models.CharField(choices=REPORT_TYPES, max_length=100)
	description = models.TextField(max_length=400)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)






        
class Post(models.Model):
    message = models.TextField(max_length=400)
    topic = models.ForeignKey(Topic, related_name='post', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True) 
    edit_date = models.DateField(null=True)
        
        
    def add_comment_notification(self, sender, topic):
        notify = Notification.objects.create(topic=topic, sender=sender, user=topic.created_by, notification_type=2)



    def delete_comment_notification(self, sender, topic):
        notify = Notification.objects.filter(topic=topic, sender=sender, user=topic.created_by, notification_type=2)
        notify.delete()    


 
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)       


