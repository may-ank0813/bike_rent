from django.db import models
from django.contrib.auth.models import User

class Bike(models.Model):
    name      = models.CharField(max_length=50,null=True, blank=True, default='Bullet')
    model      = models.CharField(max_length=70,null=True, blank=True)
    about      = models.TextField(max_length=355,null=True, blank=True)
    shortAbout = models.CharField(max_length=70,null=True, blank=True)
    topSpeed   = models.IntegerField(null=True,blank=True)
    price      = models.CharField(max_length=10,null=True,blank=True)
    bike1       = models.ImageField(null=True)
    bike2       = models.ImageField(null=True)
    bike3       = models.ImageField(null=True)   
    
    def __str__(self):
        return self.name

class Faq(models.Model):
    titlePrev = models.CharField(max_length=20, null=True)
    content   = models.TextField(max_length=375,null=True, blank=True)
    question  = models.CharField(max_length=60, null=True)

    def __str__(self):
	    return self.titlePrev


class Customer(models.Model):
    user            = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, null=True)
    phone           = models.CharField(max_length=12, null=True)
    email           = models.CharField(max_length=25, null=True)
    dateCreated     = models.DateTimeField(auto_now_add=True, null=True)
    profilePic      = models.ImageField(default="basicUser.jpg",null=True, blank=True)
   

    def __str__(self):
        return self.name


class Location(models.Model):
    pickUpPlace  = models.CharField(max_length=105, null=True)

    def __str__(self):
        return self.pickUpPlace 

class Order(models.Model):
   
    customer     = models.CharField(max_length=70,null=True)
    customerID   = models.CharField(max_length=50, null=True)
    bikeModel     = models.CharField(max_length=70,null=True)
    automobileId = models.CharField(null=True,max_length=10)
    price        = models.IntegerField(null=True,blank=False)
    startRent    = models.DateField(auto_now_add=False, null=True)
    endRent      = models.DateField(auto_now_add=False, null=True)
    orderDate    = models.DateTimeField(auto_now_add=True, null=True)
    pickUp       = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.id

class canceledOrders(models.Model):
    customerID   = models.CharField(max_length=50, null=True)
    automobileId = models.CharField(null=True,max_length=10)
    price        = models.IntegerField(null=True,blank=False)