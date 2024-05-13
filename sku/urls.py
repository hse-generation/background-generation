from django.urls import path

from . import views

urlpatterns = [
    path('<int:item_id>', views.index, name='sku'),
    path('edit_image/<int:item_id>', views.edit_image, name='edit_image'),
]

