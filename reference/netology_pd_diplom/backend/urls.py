from django.urls import path, include
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, CategoryViewSet, ShopView, BasketView, \
    AccountDetails, ContactView, OrderView, PartnerState, PartnerOrders, ConfirmAccount, ParameterView, CeleryStatus, \
    ProductInfoViewSet

# добавляем роутер для viewset классов
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductInfoViewSet, basename='products')

app_name = 'backend'
urlpatterns = [
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),
    path('partner/state/', PartnerState.as_view(), name='partner-state'),
    path('partner/orders/', PartnerOrders.as_view(), name='partner-orders'),
    path('user/register/', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm/', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/details/', AccountDetails.as_view(), name='user-details'),
    path('user/contact/', ContactView.as_view(), name='user-contact'),
    path('user/login/', LoginAccount.as_view(), name='user-login'),
    path('user/password_reset/', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm/', reset_password_confirm, name='password-reset-confirm'),
    # ссылка перенесена в router
    # path('categories', CategoryView.as_view(), name='categories'),
    path('shops/', ShopView.as_view(), name='shops'),
    # ссылка перенесена в router
    # path('products/', ProductInfoView.as_view(), name='shops'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('order/', OrderView.as_view(), name='order'),
    path('parameter/', ParameterView.as_view(), name='parameter'),
    path('status/', CeleryStatus.as_view(), name='status'),
#< url for viewset классов
    path('', include(router.urls)),
# доступ к описанию проекта из API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
#>
]
