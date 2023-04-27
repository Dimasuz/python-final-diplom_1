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


def api_test():

    url_view = 'user/register/'
    num = 1
    email = '6021185@mail.ru'
    password = f'Password_{num}'
    data ={'first_name': f'first_name_{num}',
          'last_name': f'last_name_{num}',
          'email': email,
          'company': f'company_{num}',
          'position': f'position_{num}',
          'contacts': f'contacts_{num}',
          'password': password,
          }
    base_request(url_view=url_view, method='post', data=data)

    url_view = 'user/register/confirm/'
    print('POST', url_view)
    token = input('token=')
    data= {'email': email,
           'token': token,
           }
    base_request(url_view=url_view, method='post', data=data)

    url_view = 'user/login/'
    print('POST', url_view)
    data = {'email': email,
            'password': password,
            }
    response = base_request(url_view=url_view, method='post', data=data)
    token = response['Token']

    url_view = 'user/details/'
    authorization = f"Token {token}"
    headers = {'Authorization': authorization,}
    data = {'first_name': f'first_name_{num+num}', }
    base_request(url_view=url_view, method='post', headers=headers, data=data)
    base_request(url_view=url_view, method='get', headers=headers)

    url_view = 'partner/update/'
    data = {'url': "https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml"}
    content_type = 'application/x-www-form-urlencoded'
    headers = {'Content-Type': content_type, 'Authorization': authorization,}
    base_request(url_view=url_view, method='post', headers=headers, data=data)

    url_view = 'partner/orders/'
    base_request(url_view=url_view, headers=headers)
    data = {'id': 1, 'state': 'New goods',}
    base_request(url_view=url_view, method='post', headers=headers, data=data)

    url_view = 'shops/'
    base_request(url_view=url_view)

    url_view = 'user/contact/'
    authorization = f"Token {token}"
    headers = {'Authorization': authorization, }
    data = {'city': f'city_test',
            'street': f'street_test',
            'phone': f'phone_test'
            }
    task = base_request(url_view=url_view, method='post', headers=headers, data=data)
    task_id = task['task_id']
    if task_id:
        url_view = 'status/'
        params = {'task_id': task_id}
        status = "PENDING"
        while status == "PENDING" or status == "STARTED":
            status_task = base_request(url_view=url_view, method='get', headers=headers, params=params)
            status = status_task['status']
            time.sleep(1)

    url_view = 'categories/'
    base_request(url_view=url_view)

    url_view = 'products/'
    params = {'shop_id': None,
              'category_id': None,
              'product_id': 1,
              }
    base_request(url_view=url_view, params=params)

    url_view = 'basket/'
    data = {"items": '[{"quantity": 1, "product_info": 5}, {"quantity": 1, "product_info": 4}]'}
    headers = {'Content-Type': content_type, 'Authorization': authorization, }
    base_request(url_view=url_view, method='post', headers=headers, data=data)
    base_request(url_view=url_view, headers=headers)
    data = {"items": '[{"id": 4, "quantity": 2}, {"id": 5, "quantity": 2}]'}
    base_request(url_view=url_view, method='put', headers=headers, data=data)
    base_request(url_view=url_view, headers=headers)
    data = {"items": "4,5"}
    base_request(url_view=url_view, method='delete', headers=headers, data=data)

    url_view = 'order/'
    params = {'order': 1}
    base_request(url_view=url_view, params=params)
    data = {'id': 1,
            'contact': 1,
            }
    base_request(url_view=url_view, method='post', headers=headers, data=data)

    url_view = 'parameter/'
    base_request(url_view=url_view, headers=headers)
    data = {'name': 'цвет', }
    base_request(url_view=url_view, method='post', headers=headers, data=data)
    data = {'id': 1, 'name': 'New parameter', }
    base_request(url_view=url_view, method='put', headers=headers, data=data)
    data = {'id': 1, }
    base_request(url_view=url_view, method='delete', headers=headers, data=data)
    base_request(url_view=url_view, headers=headers)

if __name__ == "__main__":
    api_test()