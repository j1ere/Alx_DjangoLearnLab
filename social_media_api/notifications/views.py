from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        unread_notifications = notifications.filter(is_read=False)

        # Mark unread notifications as read
        unread_notifications.update(is_read=True)

        return Response({
            "notifications": [
                {
                    "actor": notification.actor.username,
                    "verb": notification.verb,
                    "target": str(notification.target),
                    "timestamp": notification.timestamp,
                    "is_read": notification.is_read,
                }
                for notification in notifications
            ]
        })
