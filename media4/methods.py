import requests

def request_method(url:str,token:str, method:str, data:dict=None, file:list = None):
    r"""
    :param: url 'http://example.com'.
    :param: token as string.
    :param: method (get, post, put, delete).
    :param: data {'str': Any}.
    """

    if method.lower() == 'get':
        response = requests.get(
            url=url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    elif method.lower() == 'put':
        response = requests.put(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
            },
            data=data,
            files=file
        )

    else:
        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {token}"
            },
            data=data,
            files=file
        )

    return response
    