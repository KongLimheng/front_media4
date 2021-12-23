from .methods import request_method


def get_media(req):
    token = req.COOKIES.get('token')
    if token:
        url = 'http://3.13.99.69/api/v1/me/media/'
        req_media = request_method(url, token, 'get')
        if req_media.status_code == 200:
            return {
                'medias': req_media.json()['result']
            }

    return {
        'medias': []
    }
