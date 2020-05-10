"""
Views for testing notifications. Should not be present in production
"""
from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape
from django.views.generic import TemplateView, View

from . import registry


class TestNotificationList(TemplateView):
    """
    View for listing out all notifications with links to view rendered versions of them
    """

    template_name = "herald/test/notification_list.html"

    def get_context_data(self, **kwargs):
        context = super(TestNotificationList, self).get_context_data(**kwargs)

        context["notifications"] = [
            (index, x.__name__, x.render_types, (y.__name__ for y in x.__bases__))
            for index, x in enumerate(registry._registry)  # pylint: disable=W0212
        ]

        return context


class TestNotification(TemplateView):
    """
    View for showing rendered test notification
    """

    template_name = "herald/test/notification_detail.html"

    def get_notification(self):
        index = int(self.kwargs["index"])
        render_type = self.kwargs["type"]

        return registry._registry[index](
            *registry._registry[index].get_demo_args()
        )  # pylint: disable=W0212

    def get_content(self, obj):
        context = obj.get_context_data()
        return obj.render(self.kwargs["type"], context)

    def get_context_data(self, **kwargs):  # pylint: disable=W0613
        context = super().get_context_data(**kwargs)
        obj = self.get_notification()
        kwargs["render_type"] = "plain" if render_type == "text" else render_type
        kwargs["recipients"] = obj.get_recipients()
        kwargs["content"] = escape(self.get_content(obj))
        return kwargs


class SendTestNotification(TestNotification):
    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_notification()
            obj.send()
            return HttpResponse("Sent")
        except KeyError:
            return self.get(request, *args, **kwargs)
