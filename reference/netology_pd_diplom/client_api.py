import datetime
import time

import requests
from pprint import pprint

url_base = 'http://0.0.0.0:8000/api/v1/'

def base_request(url_view='', method='get', headers=None, data=None, params=None):
    url = url_base + url_view
    print()
    print(method, url_view)
    if method == 'get':
        response = requests.get(url, headers=headers, params=params)
    if method == 'post':
        response = requests.post(url, headers=headers, data=data,)
    if method == 'put':
        response = requests.put(url, headers=headers, data=data,)
    if method == 'delete':
        response = requests.delete(url, headers=headers, data=data,)
    print(response.status_code)
    try:
        response.json()
    except BaseException:
        print('Ошибка')
    else:
        pprint(response.json())
        return response.json()

def get_headers(content_type=None):
    token, num = login()
    authorization = f"Token {token}"
    if content_type:
        headers = {'Content-Type': content_type, 'Authorization': authorization,}
    else:
        headers = {'Authorization': authorization,}
    return headers, num


# логин -----------------------
def login(num=None):
    if not num:
        num = int(input('Введите номер пользователя (или 0) = '))
    url_view = 'user/login'
    url = url_base + url_view
    print()
    print('POST', url_view)
    if num == 0:
        email = input('Введите email пользователя = ')
        num = input('Введите номер пароля = ')
    else:
        email = f'email_{num}@mail.ru'
    password = f'Password_{num}'
    data= {'email': email,
           'password': password,
           }
    response = requests.post(url,
                             data=data,
                             )
    print(response.status_code)
    if response.status_code == 200:
        if response.json()['Status'] == False:
            print('Нет такого пользователя')
            token = None
        else:
            token = response.json()['Token']
            print(token)
            print(response.json())
    else:
        token = None
    return token, num


def user_register(num):
    url_view = 'user/register'
    url = url_base + url_view
    print('POST', url_view)
    num = int(input('Введите номер пользователя = '))
    data ={'first_name': f'first_name_{num}',
          'last_name': f'last_name_{num}',
          'email': f'email_{num}@mail.ru',
          'company': f'company_{num}',
          'position': f'position_{num}',
          'contacts': f'contacts_{num}',
          'password': f'Password_{num}',
          'type': 'shop'
          }
    response = requests.post(url,
                             data=data,
                             )
    # print(response.json())
    print(response.status_code)


# # --------------------------------'Errors': 'Неправильно указан токен или email'
def confirm(num, token):
    if token:
        url_view = 'user/register/confirm'
        data= {'email': f'email_{num}@mail.ru',
               'token': token,
               }
        base_request(url_view=url_view, method='post', data=data)


def user_details(method, data=None):
    url_view = 'user/details'
    headers, _ = get_headers()
    if method == 'post':
        k = input('Введите изменяемую характеристику: ')
        v = input('Введите значение характеристики: ')
        data = {k: v, }
    base_request(url_view=url_view, method=method, headers=headers, data=data)


def partner_state(method, data=None):
    url_view = 'partner/state'
    headers, _ = get_headers()
    if method == 'post':
        state = input('Введите state: ')
        data = {'state': state}
        base_request(url_view=url_view, method=method, headers=headers)


def partner_update(data):
    url_view = 'partner/update'
    headers, _ = get_headers(content_type='application/x-www-form-urlencoded')
    base_request(url_view=url_view, method='post', headers=headers, data=data)


def parameter(method: str = 'get', data=None):
    url_view = 'parameter'
    headers, _ = get_headers()
    if method == 'post':
        name = input('Введите новое наименование характеристики: ')
        data = {'name': name,}
    if method == 'put':
        id = int(input('Введите id характеристики: '))
        name = input('Введите новое наименование характеристики: ')
        data = {'id': id, 'name': name,}
    if method == 'delete':
        id = int(input('Введите id характеристики: '))
        data = {'id': id,}
    base_request(url_view=url_view, method=method, headers=headers, data=data)


def user_contact(method='get', data=None):
    url_view = 'user/contact'
    headers, num = get_headers()
    if method == 'post':
        data = {'city': f'city_{num}',
                'street': f'street_{num}',
                'house': f'house_{num}',
                'structure': f'structure_{num}',
                'building': f'building_{num}',
                'apartment': f'apartment_{num}',
                'phone': f'phone_{num}'
                }
    if method == 'put':
        k = input('Введите изменяемую характеристику: ')
        v = input('Введите значение характеристики: ')
        data = {k: v, }
    if method == 'delete':
        items = input('Введите id контакта (если несколько, то через зарятую без пробелов) = ')
        data = {'items': items,}
    base_request(url_view=url_view, method=method, headers=headers, data=data)


def user_contact_test(method, email, password):
    url_view = 'user/login'
    url = url_base + url_view
    data= {'email': email,
           'password': password,
           }
    response = requests.post(url,
                             data=data,
                             )
    print('login status =', response.status_code)
    if response.status_code == 200:
        if response.json()['Status'] == False:
            print('Нет такого пользователя')
            token = None
        else:
            token = response.json()['Token']
            print(f'{token=}')
    authorization = f"Token {token}"
    headers = {'Authorization': authorization, }
    if method == 'post':
        data = {'city': f'city_test',
                'street': f'street_test',
                'phone': f'phone_test'
                }
    url_view = 'user/contact'
    task = base_request(url_view=url_view, method=method, headers=headers, data=data)
    task_id = task['task_id']
    if task_id:
        url_view = 'status'
        params = {'task_id': task_id}
        status = "PENDING"
        while status == "PENDING" or status == "STARTED":
            status_task = base_request(url_view=url_view, method='get', headers=headers, params=params)
            status = status_task['status']
            time.sleep(1)

# ---------------------------------------------------

def status(task_id=None):
    if task_id:
        status = "PENDING"

        while status == "PENDING":
            status = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}").json()["status"]
            print(status)
            time.sleep(1)

# ---------------------------------
def partner_state(method, data=None):
    url_view = 'partner/state'
    headers, _ = get_headers()
    base_request(url_view=url_view, method=method, headers=headers, data=data)


def basket(method: str = 'get', data=None):
    url_view = 'basket'
    token, _ = login()
    authorization = f"Token {token}"
    content_type = 'application/x-www-form-urlencoded'
    headers = {'Content-Type': content_type, 'Authorization': authorization,}

    response = base_request(url_view=url_view, method=method, headers=headers, data=data)
    print(response)


def order(method: str = 'get', data=None):
    url_view = 'order'
    headers, _ = get_headers(content_type='application/x-www-form-urlencoded')
    if method == 'get':
        order = input('Введите id заказа или ENTER, чтобы получить все заказы: ')
        if order != '':
            order = int(order)
            params = {'order': order}
            data = None
        else:
            params = None
            data = None
    if method == 'post':
        id = int(input('Введите id корзины: '))
        contact = input('Введите id адреса доставки: ')
        data = {'id': id,
                'contact': contact,
                }
        params = None
    base_request(url_view=url_view, method=method, headers=headers, data=data, params=params)

# post
# data = {"id": id, "contact": 1}
# delete
# data = {"items": 2}


def partner_orders(method: str = 'get', data=None):
    url_view = 'partner/orders'
    headers, _ = get_headers()
    if method == 'put':
        id = int(input('Введите id товара в заказе: '))
        name = input('Введите новое значение state: ')
        data = {'id': id,
                'state': name,
                }
    base_request(url_view=url_view, method=method, headers=headers, data=data)


