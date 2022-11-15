from django.urls import path
from .views import (
    create_license, IndexView, delete_license,
    check_license, contact_view, change_contact,
    set_info, view_info, authenticate, set_help_url,
    view_help, set_message, get_message, get_proxy
)

app_name = 'web'
urlpatterns = [
    path("", IndexView.as_view(), name="index-page"),
    path("create/", create_license),
    path("delete/", delete_license),
    path("verify/", check_license),
    path("contact/", contact_view),
    path("change/", change_contact),
    path("setinfo/", set_info),
    path("viewinfo/", view_info),
    path("auth/", authenticate),
    path("set_help/", set_help_url),
    path("viewhelp/", view_help),
    path("getmsg/", get_message),
    path("setmsg/", set_message),
    path("proxy/", get_proxy)
]
