from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)

    def __str__(self):
        return self.name

class Lawyer(models.Model):
    QUALIFICATION = (
        ('',''),
        ('',''),
        ('',''),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    qualification = models.CharField(max_length=200, null=True,choices=QUALIFICATION)
    experience = models.IntegerField()
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class LegalService(models.Model):
	
    STATUS = (
			('Pending', 'Pending'),
			('Accepted', 'Accepted'),
			('Completed', 'Completed'),
			)

    DOMAIN = (
        ('',''),
        ('',''),
        ('',''),
        ('',''),
    )

    client = models.ForeignKey(Client, null=True, on_delete= models.SET_NULL)
    lawyer = models.ForeignKey(Lawyer, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    domain = models.CharField(max_length=200, null=True, choices=DOMAIN)

    def __str__(self):
    	return self.lawyer.name + self.client.name