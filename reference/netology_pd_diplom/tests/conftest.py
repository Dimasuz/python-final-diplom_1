import time
import pytest
from rest_framework.authtoken.models import Token
from backend.models import User, Shop, Category, Parameter, Product, ProductInfo, ProductParameter, ConfirmEmailToken
from model_bakery import baker

URL_BASE = 'http://127.0.0.1:8000/api/v1/'

# фикстура для api-client'а
@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


# фикстура для регистрации и получения ConfirmEmailToken
@pytest.fixture
def register_user(client):
    url_view = 'user/register/'
    url = URL_BASE + url_view
    num = time.time()
    email = f'email_{num}@mail.ru'
    password = f'Password_{num}'
    data = {'first_name': f'first_name_{num}',
            'last_name': f'last_name_{num}',
            'email': email,
            'company': f'company_{num}',
            'position': f'position_{num}',
            'password': password,
            }
    response = client.post(url,
                           data=data,
                           )
    user_id = User.objects.all().filter(email=email).values_list('id', flat=True).get()
    conform_token = ConfirmEmailToken.objects.filter(user_id=user_id).values_list('key', flat=True).get()
    user = {'status_code': response.status_code,
            'status': response.json()['Status'],
            'task_id': response.json()['task_id'],
            'email': email,
            'password': password,
            'conform_token': conform_token,
            }
    return user


# фикстура для наполенения базы данных
@pytest.fixture
def fill_base(client):
    users = []
    for i in range(4):
        if i != 0:
            user = baker.make(User,
                              type='shop',
                              is_active=True)
        else:
            user = baker.make(User,
                              is_active=True)
        token, _ = Token.objects.get_or_create(user=user)

        users.append({'id': user.id, 'email': user.email, 'token': token})
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


# фикстура логина пользователя
@pytest.fixture()
def user_create_login(client):
    user = baker.make(User, is_active=True)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token
