import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.defaults import page_not_found
from rest_framework import status
from django.conf import settings
import requests
import base64
import shutil
from django.core.files.storage import FileSystemStorage
from .methods import request_method

def notfound(req, exception):
    return page_not_found(req, exception, template_name='notfound.html')
    # return render(req, 'notfound.html', status=status.HTTP_404_NOT_FOUND)

# new feed
def index(req):
    # cache.clear()
    token = req.COOKIES.get('token')
    if token:
        response = request_method(
            f'{settings.HOST}/api/v1/user/me', token, 'get')
        return render(req, 'index.html', {'home': 1, 'profile': response.json()})

    return redirect('media4:login-page')

# login
def login_page(req):
    phone = req.POST.get('phone')
    token = req.COOKIES.get('token')
    if token:
        return redirect('/')
    else:
        if phone:
            response_otp = requests.post(
                f'{settings.HOST}/api/v1/user/login/',
                data={
                    "phone": phone,
                    "channel": "system"
                })
            if response_otp.status_code == status.HTTP_200_OK:
                print(response_otp.text)
                return render(req, 'auth/verify-otp.html', {'login_page': 1, 'phone': phone})

        return render(req, 'auth/loginpage.html', {'login_page': 1})


def signup(req):
    return render(req, 'auth/sign-up.html', {'login_page': 1})

# view profile


def profile_page(req, user_id):
    token = req.COOKIES.get('token')
    print(user_id)
    if token:
        me = request_method(f'{settings.HOST}/api/v1/user/me', token, 'post')
        if me.status_code == status.HTTP_200_OK:
            res = me.json()

            return render(req, 'profile.html', {'profile_page': 1, "profile": res})
    return redirect('/login/')


def verify_otp(req):
    otp = req.POST.get('otp')
    phone = req.POST.get('phone')
    if otp:
        response_otp = requests.post(
            f'{settings.HOST}/api/v1/user/verify/',
            data={
                "phone": phone,
                "channel": "system",
                "otp": otp
            })
        if response_otp.status_code == status.HTTP_200_OK:
            otp_data = response_otp.json()
            res = JsonResponse(otp_data)
            res.set_cookie('token', otp_data['token'])
            res.set_cookie('refresh', otp_data['refresh'])
            return res

    return render(req, 'auth/verify-otp.html', {'login_page': 1, 'phone': phone})

# update profile


def update_profile(req):
    token = req.COOKIES.get('token')
    request = req.POST
    print(request)

    file = request.get('img_type')
    file_name = request.get('edit_picture')
    BASE_DIR = settings.MEDIA_ROOT
    if file:
        format, imgStr = file.split(';base64,')
        byte_img = imgStr.encode('utf-8')

        settings.MEDIA_ROOT.mkdir(exist_ok=True)

        with open(str(BASE_DIR / file_name), 'wb') as f:
            f.write(base64.decodebytes(byte_img))

        read_file = {'avatar': open(str(BASE_DIR / file_name), 'rb')}
    else:
        read_file = None

    data = {
        "first_name": request.get('first_name'),
        "last_name": request.get('last_name'),
        "email": request.get('email'),
        "nick_name": request.get('nick_name'),
        "gender": request.get('gender'),
        "country_code": request.get('country_code'),
        "phone_number": request.get('phone_number')
    }
    new_data = {key: value for key, value in data.items() if value}

    update = request_method(
        f'{settings.HOST}/api/v1/user/me/', token, 'put', new_data, read_file)

    if update.status_code == status.HTTP_200_OK:
        data = update.json()
        if BASE_DIR.exists():
            shutil.rmtree(BASE_DIR)
        return redirect('media4:profile', user_id=data["user_id"])
    return JsonResponse(update)

# post media


def post_media(req):
    token = req.COOKIES.get('token')
    if token:
        get_files = req.FILES.lists()
        file_length = req.FILES
        post_status = req.POST.get('status')
        multiple_file = []
        if len(file_length):
            for key, file in get_files:
                for f in file:
                    fss = FileSystemStorage()
                    filename = fss.save(f.name, f)
                    directory = str(settings.MEDIA_ROOT / filename)
                    list_file = ('media', 
                        (filename, open(directory, 'rb'), 'image/jpg')
                    )
                    multiple_file.append(list_file)

        data = {
            'title': post_status
        }

        post_file = request_method(
            url=f'{settings.HOST}/api/v1/me/post/', 
            token=token,
            method='post', 
            data=data, 
            file=multiple_file
        )
        # requests.post(
        #     f'{settings.HOST}/api/v1/me/post/',
        #     headers={
        #         'Authorization': f'Bearer {token}'
        #     },
        #     data=data,
        #     files=multiple_file,
        # )

        if post_file.ok:
            if len(multiple_file):
                shutil.rmtree(settings.MEDIA_ROOT)
            return JsonResponse(post_file.json())

    return redirect('media4:login-page')


def get_media(req):
    token = req.COOKIES.get('token')
    current_page = req.GET.get('pageNumber')
    if token:
        url = f'http://3.13.99.69/api/v1/me/media/?current_page={current_page}'
        req_media = request_method(url, token, 'get')
        if req_media.status_code == 200:
            return JsonResponse(req_media.json())

# get feed from server
def feed(req):
    token = req.COOKIES.get('token')
    current_page = req.GET.get('current_page')
    if current_page:
        res = request_method(
            f'{settings.HOST}/api/v1/media/?current_page={current_page}', token, 'get')
        if res.status_code == 200:
            return JsonResponse(res.json())
    else:
        res = request_method(f'{settings.HOST}/api/v1/media/', token, 'get')
        if res.status_code == 200:
            return JsonResponse(res.json())
