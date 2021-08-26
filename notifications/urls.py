from django.urls import path
from notifications.views import ShowNOtifications, DeleteNotification


urlpatterns = [
   	path('notification/', ShowNOtifications, name='show-notifications'),
   	path('notification/<noti_id>/delete', DeleteNotification, name='delete-notification'),
]