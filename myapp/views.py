from django.shortcuts import render,redirect,get_object_or_404
from . models import RegisterModel,ProductMode
from . forms import ProductAddingForm,RegisterForm,updateform,deleteform

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StudentSerializer
from .models import Student
from rest_framework import status

              

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def product(request):
    if request.method == "POST":
        data=ProductAddingForm(request.POST,request.FILES)
        if data.is_valid():
            data.save()
            print("saved")
    return render(request,"product.html")

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            full_name=form.cleaned_data["full_name"]
            email=form.cleaned_data["email"]
            subject= "Registration Successfull"
            message= f"""
                    Hello {full_name},

                    You Have successfully completed registration!

                    thank you.


                    """
            send_mail(subject,message,
                      settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
            messages.success(request,"REGISTRATION SUCCESSFULL")
    else:
        form = RegisterForm() 
    return render(request,"register.html",{"form":form})


def dashboard(request):
    values=[0,1,2,3,4,5,6,7,8,9,10]
    mydata=RegisterModel.objects.all()
    form=RegisterModel.objects.all()
    return render(request,"dashboard.html",{"data":values, "mydata":mydata,"form":form})



def update(request,pk):
    data=RegisterModel.objects.get(id=pk)
    if request.method == "POST":
        if request.FILES.get("profile"):
            data.profile=request.FILES.get("profile")
        data.full_name=request.POST.get("full_name")
        data.user_name=request.POST.get("user_name")
        data.number=request.POST.get("number")
        data.gender=request.POST.get("gender")
        data.dob=request.POST.get("dob")
        data.email=request.POST.get("email")
        data.address=request.POST.get("address")
        data.password=request.POST.get("password")

        data.save()
    return render(request,"update.html" ,{"data":data})

def delete(request,jk):
    data=RegisterModel.objects.get(id=jk)
    if request.method=="POST":
        data.delete()
        return redirect("dashboard")

    return render(request,"delete.html")

def login(request):
    if request.method=="POST":
        name=request.POST.get("user_name")
        password=request.POST.get("password")
        
        data=RegisterModel.objects.filter(user_name=name).first()
        if data and data.password == password:
            request.session["username"]=data.user_name
            request.session["fullname"]=data.full_name
            request.session["email"]=data.email
            request.session["user_id"]=data.id

            print(request.session.items())


            response= redirect("dashboard")
            response.set_cookie("username",data.user_name,max_age=60,expires=True)
            response.set_cookie("fullname",data.full_name,max_age=3600)
            return response

    return render(request,"login.html")


def update_list(request,jk):
    user=get_object_or_404(RegisterModel,id=jk)
    if request.method=="POST":
        form=updateform(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect("dashboard")
    else:
            form=updateform(instance=user)   

    return render(request,"update_list.html",{"data":form})

def delete_list(request,pk):
    user=get_object_or_404(RegisterModel,id=pk)
    if request.method=="POST":
        user.delete()
        return redirect("dashboard")
    return render(request,"delete_list.html")


def profile(request):

    if not request.session.get("user_id"):
        return redirect("login")
    user=RegisterModel.objects.get(id=request.session["user_id"])


    return render(request,"profile.html",{"user":user})


def logout(request):
    response=redirect("login")
    response.delete_cookie("username")
    response.delete_cookie("fullname")
    return response



class StudentList(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        student=Student.objects.all()
        serializer=StudentSerializer(student,many=True)
        return Response(serializer.data)


class StudentDetail(APIView):
    def get_object(self, id):
        return get_object_or_404(Student, id=id)

    def get(self, request, id):
        stud=self.get_object(id)
        serializer=StudentSerializer(stud)
        return Response(serializer.data)


    def put(self,request, id):
        stud=self.get_object(id)
        serializer=StudentSerializer(stud,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request, id):
            stud=self.get_object(id)
            serializer=StudentSerializer(stud,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, id):
        stud=Student.objects.get(id=id)
        stud.delete()
        return Response({"message":"Deleted Successfully"},status=status.HTTP_200_OK)