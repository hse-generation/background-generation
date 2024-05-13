from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='login'),
    # path('login/', views.login, name='login'),
    # path('register/', views.register, name='register'),
    # path('users/<int:pk>', views.UsersDetailView.as_view(), name='resume'),
    # path('users/<int:pk>/update', views.UsersUpdateView.as_view(), name='resume_update'),
]