from django.urls import path
from myapp import views

urlpatterns =[
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("product/",views.product,name="product"),
    path("register/",views.register,name="register"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("update/<int:pk>/",views.update,name="update"),
    path("delete/<int:jk>",views.delete,name="delete"),
    path("login/",views.login,name="login"),
    path("updatelist/<int:jk>",views.update_list,name="update_list"),
    path("deletelist/<int:pk>",views.delete_list,name="delete_list"),
    path("profile/",views.profile,name="profile"),
    path("logout/",views.logout,name="logout"),
    path("student/",views.StudentList.as_view(),name="student"),
    path("student_details/<int:id>/",views.StudentDetail.as_view(),name="student_details")
]