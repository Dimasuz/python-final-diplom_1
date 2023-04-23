import time
from client_api import *


#'user/register'
user_register_ = 2
num = 5
if user_register_ == 1:
    user_register(num)

if user_register_ == 9:
    url_view = 'user/register/'
    url = url_base + url_view
    print('POST', url_view)
    num = 9
    email = '6021185@mail.ru'
    data ={'first_name': f'first_name_{num}',
          'last_name': f'last_name_{num}',
          'email': email,
          'company': f'company_{num}',
          'position': f'position_{num}',
          'contacts': f'contacts_{num}',
          'password': f'Password_{num}',
          'type': 'shop'
          }
    response = requests.post(url,
                             data=data,
                             )
    print(response.status_code)
    if response.json():
        print(response.json())
# -------------------------------------------------------

#'user/details'
user_details_ = 1
if user_details_ == 1:
    user_details_method = input('Введите method (get или post) = ')
    user_details(method=user_details_method)
# -------------------------------------------------------

#'user/register/confirm'
user_confirm_ = 2
num = 1
token = 'e4f774a156b3f3377422'
if user_confirm_ == 1:
    confirm(num, token)

if user_confirm_ == 9:
    url_view = 'user/register/confirm/'
    data= {'email': '6021185@mail.ru',
               'token': 'a263a7a0d56',
               }
    base_request(url_view=url_view, method='post', data=data)

# -------------------------------------------------------
#'partner/update'
partner_update_ = 2
data = {'url': "https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml"}
if partner_update_ == 1:
    partner_update(data=data)
# -------------------------------------------------------
#'partner/state'

# -----------------------------------------------------
#'partner/orders'
partner_orders_ = 2
if partner_orders_ == 1:
    partner_orders_method = 'get'
    partner_orders(partner_orders_method, data=None)
# --------------------------------------------------------
#'shops'
shops_ = 2
if shops_ == 1:
    url_view = 'shops/'
    base_request(url_view=url_view)
# -------------------------------------------------------



# -------------------------------------------------------

#'user/contact'
user_contact_ = 2

if user_contact_ == 1:
    user_contact_method = input('Введите method (get, post, put, delete) = ')
    user_contact(user_contact_method)

if user_contact_ == 11:
    user_contact_test(method='post', email='dluzanov@mail.ru', password='Password_1')

# -------------------------------------------------------
#'user/login'
user_login_ = 2
num = 5
if user_login_ == 1:
    login(num)
# -------------------------------------------------------
#'user/password_reset'
# -------------------------------------------------------
#'user/password_reset/confirm'
# -------------------------------------------------------
#'categories'
categories_ = 2
url_view = 'categories/'
if categories_ == 1:
    base_request(url_view=url_view)
# -------------------------------------------------------

#'products'
products_ = 2
if products_ == 1:
    url_view = 'products/'
    shop_id = int(input('Введите shop_id = '))
    if shop_id == 0:
        shop_id = None
    category_id = int(input('Введите category_id = '))
    if category_id == 0:
        category_id = None
    product_id = int(input('Введите product_id = '))
    if product_id == 0:
        product_id = None
    params = {
        'shop_id': shop_id,
        'category_id': category_id,
        'product_id': product_id,
    }
    base_request(url_view=url_view, params=params)
# -------------------------------------------------------
#'basket'
basket_ = 2
if basket_ == 1:
    # basket_method = 'get'
    # data = None
    basket_method = 'post'
    data = {"items": '[{"quantity": 1, "product_info": 5}, {"quantity": 1, "product_info": 4}]'}
    # basket_method = 'put'
    # data = {"items": '[{"id": 4, "quantity": 2}, {"id": 5, "quantity": 2}]'}
    # basket_method = 'delete'
    # data = {"items": "4,5"}
    basket(basket_method, data=data)
# -------------------------------------------------------
#'order'
order_ = 2
if order_ == 1:
    order_method = input('Введите method (get, post, put, delete) = ')
    order(order_method, data=None)
# -------------------------------------------------------
#------ добавленны views
#'parameter'
parameter_ = 2
if parameter_ == 1:
    parameter_method = 'get'
    parameter(parameter_method)
    parameter_method = 'post'
    parameter(parameter_method)
    parameter_method = 'get'
    parameter(parameter_method)
    parameter_method = 'put'
    parameter(parameter_method)
    parameter_method = 'get'
    parameter(parameter_method)
    parameter_method = 'delete'
    parameter(parameter_method)
    parameter_method = 'get'
    parameter(parameter_method)



#----------------------------------------------------------------
"""
изменения кода для запуска проекта:
1. signals.py
заменено:
# new_user_registered = Signal(
#     providing_args=['user_id'],
# )
#
# new_order = Signal(
#     providing_args=['user_id'],
# )
на:
new_user_registered = Signal('user_id')
new_order = Signal('user_id')

"""
#-----------------------------------------------------------------
"""
Необходимо сделать:
+1. изменение статусов заказа администратором;
+2. добавить поле стоимости доставки;
+3. получение одного заказа покупателем;
4. отправка администраторам информации о новом заказе;
+5. добавить возможность возможность добавления (удаление, изменение) характеристик товаров.

Реализованы API Views
+ Вход
+ Регистрация
+ Список товаров
+ Карточка товара
+ Корзина
+ Подтверждение заказа
?- Спасибо за заказ
+ Заказы
+ Заказ

Корректно отрабатывает следующий сценарий:
+ пользователь может авторизироваться;
+ есть возможность отправки данных для регистрации и получения email с подтверждением регистрации;
+ пользователь может добавлять в корзину товары от разных магазинов;
+ пользователь может подтверждать заказ с вводом адреса доставки;
+ пользователь получает email с подтверждением после ввода адреса доставки;
+ Пользователь может открывать созданный заказ.

"""
#-----------------------------------------------------------------
""" 
добавления в код:

views.py

2. в класс OrderView(APIView):
метод GET добавлено - получение одного заказа покупателем (528-537);
3. добавлен класс ParametrView - возможность добавления (удаление, изменение) настраиваемых полей 
(характеристик) товаров.
4. добавлена отправка email при создании нового контакта (470), 
для этого в Signals добавлена функция new_contact_signal 
5. добавлено изменение статуса позиции в заказе поставщиком

models.py
4. в таблицу Shop добавлен параметр delivery -'Цена доставки поставщиком'.
5. В таблице OrderItem добавлено поле 'state' для возможности включения в один заказ 
товаров от разных поставщиков. А в таблице Order исключена возможность проставления статуса выше, чем 'new'.
После формирования заказа изменение статуса происходит по каждой позициии заказа соответствующим магазином. 

signals.py
добавлана функция отправки почты при добавлении контакта

"""



#----------------------------------------------------------------
