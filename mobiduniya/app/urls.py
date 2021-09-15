from django.contrib import auth
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm
urlpatterns = [
    # path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('samsung/',views.samsung,name='samsung'),
    path('samsung/<slug:data>',views.samsung,name='samsungdata'),
    path('vivo/',views.vivo,name='vivo'),
    path('vivo/<slug:data>',views.vivo,name='vivodata'),
    path('oppo/',views.oppo,name='oppo'),
    path('oppo/<slug:data>',views.oppo,name='oppodata'),
    path('mi/',views.mi,name='mi'),
    path('mi/<slug:data>',views.mi,name='midata'),
    path('realme/',views.realme,name='realme'),
    path('realme/<slug:data>',views.realme,name='realmedata'),
    path('oneplus/',views.oneplus,name='oneplus'),
    path('oneplus/<slug:data>',views.oneplus,name='oneplusdata'),   
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),


     path('password-reset-confirm/<uid64>',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),





    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
