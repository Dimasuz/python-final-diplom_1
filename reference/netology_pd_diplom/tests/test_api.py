import time
import pytest
from model_bakery import baker
import warnings
from backend.models import Shop, User, Category


warnings.filterwarnings(action="ignore")

pytestmark = pytest.mark.django_db

URL_BASE = 'http://127.0.0.1:8000/api/v1/'


def base_request(client, url_view='', method='get', token=None, data=None, params=None,):
    url = URL_BASE + url_view
    if token:
        headers = {'Authorization': f"Token {token}", }
    else:
        headers = None
    if method == 'get':
        response = client.get(url, headers=headers, params=params)
    if method == 'post':
        response = client.post(url, headers=headers, data=data,)
    if method == 'put':
        response = client.put(url, headers=headers, data=data,)
    if method == 'delete':
        response = client.delete(url, headers=headers, data=data,)
    try:
        response.json()
    except BaseException:
        print('Ошибка json')
    else:
        return response.status_code, response.json()


def test_example():
    assert True, "Just test example"


# check /api/v1/user/register
def test_user_register(user_create):
    user = user_create
    assert user['status_code'] == 200
    assert user['status'] == True


# check /api/v1/user/login
def test_login(client, user_create):
    user = user_create
    email = user['email']
    password = user['password']
    # user login
    url_view = 'user/login'
    url = URL_BASE + url_view
    data = {'email': email,
            'password': password,
            }
    response = client.post(url,
                           data=data,
                           )
    if response.status_code == 200:
        if response.json()['Status'] == False:
            token = None
        else:
            token = response.json()['Token']
    else:
        token = None

    assert token != None


# 'parameter'
def test_parameter(client, user_create_login):
    url_view = 'parameter'
    token = user_create_login['token']
    # post
    name = f'name_{time.time()}'
    data = {'name': name,}
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    assert status == 200
    # get
    status, response_json = base_request(client, url_view=url_view, method='get', token=token)
    assert status == 200
    assert response_json[0]['name'] == name
    # put
    id = int(response_json[0]['id'])
    name_new = response_json[0]['name'] + 'test'
    data = {'id': id, 'name': name_new,}
    status, response_json = base_request(client, url_view=url_view, method='put', token=token, data=data)
    assert status == 200
    # get
    status, response_json = base_request(client, url_view=url_view, method='get', token=token)
    assert status == 200
    assert response_json[0]['name'] == name_new
    # delete
    id = int(response_json[0]['id'])
    print(type(id))
    print(id)
    data = {'id': id,}
    print(data)
    status, response_json = base_request(client, url_view=url_view, method='delete', token=token, data=data)
    assert status == 200
    # get
    status, response_json = base_request(client, url_view=url_view, method='get', token=token)
    assert status == 200
    assert response_json == []


# 'categories'
def test_categories(client):
    url_view = 'categories'
    categories = baker.make(Category, make_m2m=True, _quantity=5)
    response_status, response_json = base_request(client=client, url_view=url_view)
    assert response_status == 200
    assert len(response_json['results']) == len(categories)


#'shops'
def test_shops(client):
    url_view = 'shops'
    shops = baker.make(Shop, make_m2m=True, _quantity=5)
    response_status, response_json = base_request(client=client, url_view=url_view)
    assert response_status == 200
    assert len(response_json['results']) == len(shops)


# 'user/details'
def test_user_details(client, user_create_login):
    url_view = 'user/details'
    token = user_create_login['token']
    # get
    status, response_json = base_request(client, url_view=url_view, method='get', token=token)
    assert status == 200
    assert response_json != None
    # post
    last_name = response_json['last_name'] + f'test{time.time()}'
    data = {'last_name': last_name,}
    status_post, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    # get
    status, response_json = base_request(client, url_view=url_view, method='get', token=token)
    assert status_post == 200
    assert response_json['last_name'] == last_name


#'products'
def test_products(client, fill_base):
    products = fill_base
    url_view = 'products'
    # get все товары
    response_status, response_json = base_request(client=client, url_view=url_view)
    assert response_status == 200
    assert len(response_json) == 2
    # get один товар
    params = {'product_id': 1,}
    response_status, response_json = base_request(client=client, url_view=url_view, params=params)
    assert response_status == 200


def test_user_contact(client, user_create_login):
    url_view = 'user/contact'
    user = user_create_login
    token = user_create_login['token']
    num = 1
    # post
    data = {'city': f'city_{num}',
        'street': f'street_{num}',
        'house': f'house_{num}',
        'structure': f'structure_{num}',
        'building': f'building_{num}',
        'apartment': f'apartment_{num}',
        'phone': f'phone_{num}'
        }
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    assert status == 200
    assert response_json['Status'] == True
    assert response_json['task_id'] != None
    status, response_json = base_request(client, url_view=url_view, token=token)
    id = response_json[0].pop('id')
    assert response_json[0] == data
    #put
    key = 'city'
    value = 'city_test_put'
    data = {'id': id, key: value, }
    status, response_json = base_request(client, url_view=url_view, method='put', token=token, data=data)
    assert status == 200
    assert response_json['Status'] == True
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert response_json[0][key] == value
    # delete
    data = {'items': id,}
    status, response_json = base_request(client, url_view=url_view, method='delete', token=token, data=data)
    assert status == 200
    assert response_json['Status'] == True
    assert response_json['Удалено объектов'] == 1
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert response_json == []


def test_basket(client, fill_base):
    users = fill_base
    user_auth = User.objects.get(email=users[0]['email'])
    client.force_authenticate(user=user_auth)
    token = users[0]['token']
    url_view = 'basket'
    # post
    data = {'items': '[{"quantity": 1, "product_info": 1}, {"quantity": 1, "product_info": 2}]'}
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    assert response_json['Status'] == True
    assert response_json['Создано объектов'] == 2
    # get
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert len(response_json[0]['ordered_items']) == 2
    # put
    data = {"items": '[{"id": 2, "quantity": 1}]'}
    status, response_json = base_request(client, url_view=url_view, method='put', token=token, data=data)
    assert response_json['Status'] == True
    assert response_json['Обновлено объектов'] == 1
    # get
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert response_json[0]['ordered_items'][1]['product_info']['quantity']== 2
    # delete
    data = {"items": "1"}
    status, response_json = base_request(client, url_view=url_view, method='delete', token=token, data=data)
    assert response_json['Status'] == True
    assert response_json['Удалено объектов'] == 1
    # get
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert len(response_json[0]['ordered_items']) == 1


def test_order(client, fill_base):
    # создание корзины
    users = fill_base
    url_view = 'products'
    response_status, response_json = base_request(client=client, url_view=url_view)
    token = users[0]['token']
    url_view = 'basket'
    # post
    data = {'items': '[{"quantity": 1, "product_info": 1}, {"quantity": 1, "product_info": 2}]'}
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    # get
    status, response_json = base_request(client, url_view=url_view, token=token)
    basket_id = response_json[0]['id']
    # создание контакта
    url_view = 'user/contact'
    data = {'city': f'city_',
            'street': f'street_',
            'house': f'house_',
            'structure': f'structure_',
            'building': f'building_',
            'apartment': f'apartment_',
            'phone': f'phone_'
            }
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    status, response_json = base_request(client, url_view=url_view, token=token)
    contact = response_json[0]['id']
    # post - создание заказа
    data = {'id': basket_id,
            'contact': contact,
            }
    url_view = 'order'
    status, response_json = base_request(client, url_view=url_view, method='post', token=token, data=data)
    assert status == 200
    assert response_json['Status'] == True
    assert response_json['task_id'] != None
    status, response_json = base_request(client, url_view=url_view, token=token)
    assert status == 200
    status, response_json = base_request(client, url_view=url_view, token=token, params={'order': 1})
    assert status == 200
    assert response_json[0]['id'] == 1

    'partner/orders'
    url_view = 'partner/orders'
    # get
    # получить все заказы поставщика
    num_list = [1, 2]
    shop_list = []
    order_items_id = []
    for num in num_list:
        user_auth = User.objects.get(email=users[num]['email'])
        client.force_authenticate(user=user_auth)
        token = users[num]['token']
        status, response_json = base_request(client=client, url_view=url_view, token=token)
        shop_list.append(response_json[0]['ordered_items'][0]['product_info']['shop'])
        order_items_id.append(response_json[0]['ordered_items'][0]['id'])
    assert num_list == shop_list
    # put
    # попытка изменить статус позиции в заказе другого поставщика
    state = 'confirmed'
    data = {'id': order_items_id[0], 'state': state}
    status, response_json = base_request(client, url_view=url_view, method='put', token=token, data=data)
    assert response_json['Status'] == False
    assert response_json['Errors'] == 'Нет запрашиваемого объекта или у него другой поставщик'

    # изменить статус позиции в заказе поставщика
    state = 'confirmed'
    data = {'id': order_items_id[1], 'state': state}
    status, response_json = base_request(client, url_view=url_view, method='put', token=token, data=data)
    status, response_json = base_request(client=client, url_view=url_view, token=token)
    assert status == 200
    assert response_json[0]['ordered_items'][0]['state'] == state
