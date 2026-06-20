from django.urls import path
from .views import MessageViewSet

urlpatterns = [
    path("", MessageViewSet.as_view({"get": "list", "post": "create"})),
    path("unread-count/", MessageViewSet.as_view({"get": "unread_count"})),
    path("dialog/<int:user_id>/", MessageViewSet.as_view({"get": "dialog"})),
    path("<int:pk>/read/", MessageViewSet.as_view({"post": "read"})),
]
