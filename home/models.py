from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
       return self.username


   
class StayPics(models.Model):

    room = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.room


# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.core.files.base import ContentFile
# from django.core.files import File
# from PIL import Image
# import io
# from storages.backends.s3boto3 import S3Boto3Storage

# class User(AbstractUser):
    
#     USERNAME_FIELD = 'username'
    
#     def __str__(self):
#        return self.username


   
# class StayPics(models.Model):

#     room = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='images/')
    
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.image:
#             storage = S3Boto3Storage()
#             with storage.open(self.image.name, 'rb') as image_file:
#                 img = Image.open(image_file)
#                 if img.height > 85 or img.width > 85:
#                     output_size = (85, 85)
#                     img.thumbnail(output_size)
#                     in_memory_file = io.BytesIO()
#                     img.save(in_memory_file, format=img.format)
#                     in_memory_file.seek(0)
#                     # Save the resized image back to the S3 bucket
#                     storage.save(self.image.name, File(in_memory_file))
    
#     def __str__(self):
#         return self.room




class DinePics(models.Model):
    
    LUNCH = 'Lunch'
    EVENING = 'Evening'
    DINNER = 'Dinner'
    
    meal_choices = [
        (LUNCH, 'Lunch'),
        (EVENING,'Evening'),
        (DINNER, 'Dinner')
    ]

    meal_time = models.CharField(max_length=10, choices=meal_choices)
    meal_type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    
    def __str__(self):
        return self.name    



  
  
  
  
# hotel_manager_group,created = Group.objects.get_or_create(name='Hotel Manager')
# receptionist_group,created = Group.objects.get_or_create(name='Receptionist')
# staff_group,created = Group.objects.get_or_create(name='staff')


# manage_hotel =Permission.objects.get(name='manage_hotel')
# check_guest = Permission.objects.get(codename='check_guest') ####
# can_clean = Permission.objects.get(name = 'can_clean')


# hotel_manager_group.permissions.add(manage_hotel)
# receptionist_group.permissions.add(check_guest)
# staff_group.permissions.add(can_clean)


# user = User.objects.get(username = 'calix')
# user.groups.add(manage_hotel)


# dinner = DinePics(meal_type=DinePics.DINNER, start_time=time(18, 30), end_time=time(23, 0))








