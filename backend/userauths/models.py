from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver


#Here we are creating a new model for the user of our api
class User(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(unique=True)
    
    #this parameter have null and blank true, that means that this model dont need that
    #information for make an object
    fullname=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    
    #This line specifies that the email field (email) should be used as the unique identifier for authentication purposes instead of the default username field. This means that when users log in, they'll provide their email address instead of a username.
    USERNAME_FIELD='email'
    
    # This line specifies which additional fields are required when creating a user via the createsuperuser management command
    REQUIRED_FIELDS=['username']
    
    #return self.email: This line specifies that when the __str__ method is called on a User object, it should return the email address (self.email) of that user.
    def __str__(self):
        return self.email

    #this function when its gonna save an user replace the fullname or the username if this atributes does not have a value
    def save(self,*args,**kwargs):
        email_username,mobile=self.email.split("@")
        if self.fullname == "" or self.fullname == None:
            self.fullname = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User,self).save(*args,**kwargs)

#this model is a profile that is related to the user
class Profile(models.Model):
    
    #This line defines a field named user. It's a OneToOneField, which means each instance of the Profile class will be associated with exactly one instance of the User class (likely the custom user model you defined earlier).
    #on_delete=models.CASCADE specifies the behavior when the referenced User object is deleted. In this case, it's set to CASCADE, meaning if a User object is deleted, the associated Profile object will also be deleted.
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.FileField(upload_to="image",default="default/default-user.jpg",null=True,blank=True)
    fullname=models.CharField(max_length=100,null=True,blank=True)
    about=models.TextField(null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    pid=ShortUUIDField(unique=True,length=10,max_length=20,alphabet="abcdefghijk")
    
    def __str__(self):
        if self.fullname:
            return str(self.fullname)
        else:
            return str(self.user.fullname)
        
    def save(self,*args,**kwargs):
        if not self.fullname:
            self.fullname = self.user.fullname
        try:
            super(Profile, self).save(*args, **kwargs)
        except:
            pass 

#this are the signals it activates when a user is save
@receiver(post_save, sender=User)        
def create_user_profile(sender,instance,created,**kwargs):
    #this condition says that if the user was created, then create a profile and asing to the atribute user the instance that was just created
    if created:
        Profile.objects.create(user=instance)

#then when a the function above finish,Inside the function, it tries to save the associated Profile instance of the User. It assumes that each User instance has a related Profile instance (due to the one-to-one relationship defined earlier).       
@receiver(post_save, sender=User)
def save_user_profile(sender,instance,**kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass