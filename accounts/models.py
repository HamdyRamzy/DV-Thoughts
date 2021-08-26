from django.db import models



class Owner(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to='photos/%y/%m/%d')
    facebook = models.URLField(max_length = 200, blank=True, null=True)
    github = models.URLField(max_length = 200, blank=True, null=True)
    linkedin = models.URLField(max_length = 200, blank=True, null=True)

    def __str__(self):
        return self.name
    

