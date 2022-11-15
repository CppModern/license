from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http.request import HttpRequest
from .models import License, gen_license
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from configparser import ConfigParser
from .models import Contact
from .models import Messagebox
from .models import Proxy


User = get_user_model()
config = ConfigParser()
config.read("web/contact.ini")


class IndexView(TemplateView):
    template_name = "web/index.html"


@csrf_exempt
def create_license(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    api_hash = request.POST.get("hash", None)

    if not api_hash:
        return JsonResponse({"error": "authentication failed"})
    key = gen_license()
    user = User.objects.get(id=1)
    License.objects.create(key=key, created_by=user)
    return JsonResponse({"key": key})


@csrf_exempt
def delete_license(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    key = request.POST.get("key")
    if not key:
        return JsonResponse({"error": "No key provided"})
    if not key.isdigit():
        return JsonResponse({"error": "invalid key"})
    try:
        llc = License.objects.get(key=key)
    except License.DoesNotExist:
        return JsonResponse({"error": "invalid key"})
    else:
        llc.delete()
        return JsonResponse({"success": key})


@csrf_exempt
def check_license(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    key = request.POST.get("key").strip()
    if not key.isdigit():
        return JsonResponse({"error": "invalid key"})
    if not key:
        return JsonResponse({"error": "No key provided"})
    try:
        llc = License.objects.get(key=key)
    except License.DoesNotExist:
        return JsonResponse({"error": "invalid key"})
    mac = request.POST.get("mac")
    if llc.used and (llc.mac != mac):
        return JsonResponse(
            {"error": "This key has already been used in another device"}
        )
    else:
        llc.used = True
        llc.mac = mac
        llc.save()
        return JsonResponse({"success": key})


def contact_view(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "method pot allowed"})
    contact = Contact.objects.get(id=1)
    url = contact.url
    return JsonResponse({"link": url})


@csrf_exempt
def change_contact(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    contact = "https://t.me/"
    user = request.POST.get("contact")
    if not user:
        return JsonResponse({"error": "must provide a new contact"})
    contact = contact + user
    try:
        old = Contact.objects.get(id=1)
    except Contact.DoesNotExist:
        Contact.objects.create(url=contact)
    else:
        old.url = contact
        old.save()
    return JsonResponse({"success": contact})


@csrf_exempt
def set_info(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    info = request.POST.get("info")
    if not info:
        return JsonResponse({"error": "no information provided"})
    contact = Contact.objects.get(id=1)
    contact.key_info = info
    contact.save()
    return JsonResponse({"success": "new information set"})


def view_info(request: HttpRequest):
    info = Contact.objects.get(id=1)
    return JsonResponse({"info": info.key_info})


def view_help(request: HttpRequest):
    help = Contact.objects.get(id=1)
    return JsonResponse({"link": help.key_help_link})


@csrf_exempt
def set_help_url(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"})
    link = request.POST.get("link", "")
    if not link:
        return JsonResponse({"error": "no data provided"})
    contact = Contact.objects.get(id=1)
    contact.key_help_link = link
    contact.save()
    return JsonResponse({"success": f"{link}"})


@csrf_exempt
def authenticate(request: HttpRequest):
    user = User.objects.get(id=1)
    pwd = request.POST.get("pwd", "")
    if user.check_password(pwd):
        return JsonResponse({"success": f"{pwd}"})
    return JsonResponse({"error": "invalid password"})



def get_message(request: HttpRequest):
    try:
        text = Messagebox.objects.get(id=1).text
    except Exception:
        text = "Welcome to Auttg"
    return JsonResponse({"text": text})


@csrf_exempt
def set_message(request: HttpRequest):
    if not request.method == "POST":
        return JsonResponse({"error": "method not allowed"})
    text = request.POST.get("text")
    try:
        msgbox: Messagebox = Messagebox.objects.get(id=1)
        msgbox.text = text
    except:
        msgbox = Messagebox.objects.create(text=text)
    msgbox.save()
    return JsonResponse({"success": "Data updated"})


def get_proxy(request: HttpRequest):
    try:
        proxy: Proxy = Proxy.objects.get(id=1)
    except:
        return JsonResponse({"error": "no proxy available"})
    data = [proxy.host, proxy.port, proxy.username, proxy.password]
    return JsonResponse({"proxy": data})
