from django.urls import path
from profiles_api import views

# .as_view is a standard function to would render the view.py file's HelloApiView class for a http request
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),

]
