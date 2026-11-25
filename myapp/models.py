from django.db import models

class ProductMode(models.Model):
    image=models.ImageField(upload_to="product_image/")
    product_name=models.CharField(max_length=50)
    price=models.FloatField()
    quantity=models.IntegerField()
    product_des=models.TextField(max_length=500)



class RegisterModel(models.Model):
    profile=models.ImageField(upload_to="profile_image/")
    full_name=models.CharField(max_length=50)
    user_name=models.CharField(max_length=30)
    number=models.IntegerField()
    choose=[
        ("Male","Male"),
        ("Female","Female")
    ]

    gender=models.CharField(max_length=30)
    dob=models.DateField()
    email=models.EmailField()

    password=models.CharField(max_length=20)

    def __str__(self):
        return self.user_name




class Student(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    age=models.IntegerField()
    department=models.CharField(max_length=50)
    