from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification

def ShowNOtifications(request):
	if request.user.is_authenticated:
		user = request.user
		notifications = list(Notification.objects.filter(user=user).order_by('-date'))

		return  {'notifications': notifications}
	return{}


def DeleteNotification(request, noti_id):
	user = request.user
	Notification.objects.filter(id=noti_id, user=user).delete()
	return redirect('home')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

		return {'count_notifications':count_notifications}
	return{}
	