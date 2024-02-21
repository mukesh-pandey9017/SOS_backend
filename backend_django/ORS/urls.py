from django.urls import path,re_path
from . import views

urlpatterns = [
    path("",views.index),
    path('<page>/',views.actionId),
    path("<page>/<operation>/<int:id>/", views.actionId),
    path("auth/<page>/", views.auth)

]