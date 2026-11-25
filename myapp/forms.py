from django import forms
import re
from . models import ProductMode,RegisterModel
from datetime import date

class ProductAddingForm(forms.ModelForm):
    class Meta:
        model=ProductMode
        fields="__all__"


class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=RegisterModel
        fields="__all__"

    def clean_full_name(self):
        fullname=self.cleaned_data["full_name"]
        if len(fullname) < 3:
            raise forms.ValidationError("Please enter a valid name!")
        return fullname

    def clean_email(self):
        email=self.cleaned_data["email"]
        if RegisterModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Already created an account using this email!!")
        return email

    def clean_user_name(self):
        username=self.cleaned_data["user_name"]
        if RegisterModel.objects.filter(user_name=username).exists():
            raise forms.ValidationError("User name already exists")
        if len(username)<4:
            raise forms.ValidationError("length of username should be greater than 4")
        return username

    def clean_number(self):
        number=self.cleaned_data["number"]
        if RegisterModel.objects.filter(number=number).exists():
                raise forms.ValidationError("Already registered using this phone number")
        if len(str(number))<10 or len(str(number))>11:
                raise forms.ValidationError("Please enter a valid Phone number")
        return number

    def clean_dob(self):
         dob=self.cleaned_data["dob"]
         today=date.today()
         if dob>today :
              raise forms.ValidationError("Date of birth cannot be in future")

         return dob
    def clean_password(self):
         password=self.cleaned_data["password"]
         if len(password) <8:
              raise forms.ValidationError("Password must contain atlest 8 characters!")
         if not re.search(r'[A-Z]',password):
              raise forms.ValidationError("Password must contain atleast one Uppercase letter")
         if not re.search(r'[a-z]',password):
                       raise forms.ValidationError("Password must contain atleast one Lowercase letter")
         if not re.search(r'[0-9]',password):
                       raise forms.ValidationError("Password must contain atleast one Digit")
         if not re.search(r'[@!%$&*()/_^]',password):
                       raise forms.ValidationError("Password must contain atleast one Special character")

         return password

    def clean(self):
          data=super().clean()
          password=data.get("password")
          confirm_password=data.get("confirm_password")
          if password and confirm_password:
                if password != confirm_password:
                      self.add_error("confirm_password","Passwords Misatch")
          return data

class updateform(forms.ModelForm):
      class Meta:
            model=RegisterModel
            fields="__all__"
class deleteform(forms.ModelForm):
      class Meta:
            model=RegisterModel
            fields="__all__"