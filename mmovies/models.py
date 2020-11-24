from django.db import models
from django.contrib.auth.models import User

class sections(models.Model):
    name = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

#-----------------------------------------------

class all(models.Model):
    ch=(
        ('movie','Movie'),
        ('series','Series')
    )
    name= models.CharField(max_length=100,null=True)
    shortname=models.CharField(max_length=16,null=True)
    img = models.ImageField()
    rate = models.FloatField(null=True)
    story= models.TextField(null=True)
    trailer = models.URLField(null=True,blank=True)
    type = models.CharField(max_length=100,null=True,choices=ch)
    section = models.ManyToManyField(sections)
    watchlist_in = models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.name

#-----------------------------------------------

class actors(models.Model):
    name= models.CharField(max_length=100,null=True)
    img = models.ImageField(null=True)
    wikilink = models.URLField(null=True,blank=True)
    roles = models.ManyToManyField(all)
    def __str__(self):
        return self.name

#-----------------------------------------------

class user_watchlist_parent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class  user_watchlist_child(models.Model): 
    d = models.ForeignKey(all,null=True,on_delete=models.CASCADE)
    u = models.ForeignKey(user_watchlist_parent,null=True,on_delete=models.CASCADE)  
    watchcheck=models.BooleanField(default=False)
    def __str__(self):
        return self.u.user.username+" / "+ self.d.name