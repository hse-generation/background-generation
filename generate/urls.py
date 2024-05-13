from django.urls import path

from . import views

urlpatterns = [
    path('<int:item_id>', views.index, name='generate'),
    path('generate_image/', views.generate_image, name='generate_image'),
    path('flip_image/', views.flip_image, name='flip_image'),
    path('add_text/', views.add_text, name='add_text'),
    path('save_image/<int:item_id>/', views.save_image, name='save_image'),
]


