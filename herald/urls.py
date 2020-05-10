"""
Urls for herald app
"""

from django.conf.urls import url

from .views import SendTestNotification, TestNotification, TestNotificationList

urlpatterns = [
    url(r"^$", TestNotificationList.as_view(), name="herald_preview_list"),
    url(
        r"^(?P<index>\d+)/(?P<type>[\w\-]+)/$",
        TestNotification.as_view(),
        name="herald_preview",
    ),
    url(
        r"^(?P<index>\d+)/(?P<type>[\w\-]+)/send/$",
        SendTestNotification.as_view(),
        name="send_test_notification",
    ),
]
