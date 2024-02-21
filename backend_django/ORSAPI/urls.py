from django.urls import path
from ORSAPI import views

urlpatterns = [
    path('<page>/<action>', views.action),
    path('<page>/<action>/', views.action),
    path('<page>/<action>/<int:id>', views.action)
]