import time
import pytest
from backend.models import User, Shop, Category, Parameter, Product, ProductInfo, ProductParameter


URL_BASE = 'http://127.0.0.1:8000/api/v1/'

# фикстура для api-client'а
@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


# фикстура для наполенения базы данных
@pytest.fixture
def fill_base(client):
    users = []
    for i in range(4):
        num = i + 1
        url_view = 'user/register/'
        url = URL_BASE + url_view
        data = {'first_name': f'first_name_{num}',
                'last_name': f'last_name_{num}',
                'email': f'email_{num}@mail.ru',
                'company': f'company_{num}',
                'position': f'position_{num}',
                'contacts': f'contacts_{num}',
                'password': f'Password_{num}'
                }
        client.post(url, data=data,)
        user =  {'email': f'email_{num}@mail.ru',
                'password': f'Password_{num}',
                 'type': 'buyer',
                }
        url_view = 'user/login/'
        url = URL_BASE + url_view
        data = {'email': user['email'],
                'password': user['password'],
                }
        response = client.post(url,
                               data=data,
                               )
        user['token'] = response.json()['Token']
        user_auth = User.objects.get(email=user['email'])
        client.force_authenticate(user=user_auth)
        url_view = 'user/details/'
        url = URL_BASE + url_view
        response = client.get(url, headers={'Authorization': f"Token {user['token']}", }, )
        user['id'] = response.json()['id']
        if num != 1:
            authorization = f"Token {user['token']}"
            headers = {'Authorization': authorization, }
            client.post(url, headers=headers, data={'type': 'shop', })
            user['type'] = 'shop'
        users.append(user)
    for num in [1, 2]:
        shop = users[num]
        data = {'shop': f'shop_{num}',
                'categories': [{'id': num, 'name': f'categories_{num}'},
                               {'id': int(f'{num}{num}'), 'name': f'categories_{num}{num}'},
                               {'id': int(f'{num}{num}{num}'), 'name': f'categories_{num}{num}{num}'},
                               ],
                'goods': [{'id': num, 'category': num, 'model': f'model_{num}', 'name': f'name_model_{num}',
                           'price': int(f'{num}000'), 'price_rrc': int(f'{num}00'), 'quantity': num,
                           'parameters': {"parameters_1": f'parameters_1_{num}',
                                          "parameters_2": f'parameters_2_{num}',
                                          },
                           },
                          ],
                }
        shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=shop['id'])
        for category in data['categories']:
            category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
            category_object.shops.add(shop.id)
            category_object.save()
        for item in data['goods']:
            product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
            product_info = ProductInfo.objects.create(product_id=product.id,
                                                      external_id=item['id'],
                                                      model=item['model'],
                                                      price=item['price'],
                                                      price_rrc=item['price_rrc'],
                                                      quantity=item['quantity'],
                                                      shop_id=shop.id)
            for name, value in item['parameters'].items():
                parameter_object, _ = Parameter.objects.get_or_create(name=name)
                ProductParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter_object.id,
                                                value=value)
    return users


# фикстура создания пользователя
@pytest.fixture()
def user_create(client):
    url_view = 'user/register/'
    url = URL_BASE + url_view
    num = time.time()
    data ={'first_name': f'first_name_{num}',
          'last_name': f'last_name_{num}',
          'email': f'email_{num}@mail.ru',
          'company': f'company_{num}',
          'position': f'position_{num}',
          'contacts': f'contacts_{num}',
          'password': f'Password_{num}'
          }
    response = client.post(url,
                             data=data,
                             )
    return {'status_code': response.status_code,
            'status': response.json()['Status'],
            'email': f'email_{num}@mail.ru',
            'password': f'Password_{num}',
             }


# фикстура логина пользователя
@pytest.fixture()
def user_create_login(client, user_create):
    url_view = 'user/login/'
    url = URL_BASE + url_view
    user = user_create
    email = user['email']
    password = user['password']
    data= {'email': email,
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
            user_auth = User.objects.get(email=email)
            client.force_authenticate(user=user_auth)
    else:
        token = None
    user['token'] = token
    return user
