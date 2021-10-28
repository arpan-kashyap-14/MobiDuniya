from django.contrib import auth
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    # path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('suggest/product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('user/',views.dashboard,name='dashboard'),
    path('compare/',views.compare,name='compare'),
    path('compare/getProduct',views.getproduct,name='getproduct'),
    path('productviewcompare/getProduct',views.getproduct,name='getproductview'),
    path('compare/showProducts',views.compareshowproducts,name='compareshowproduct'),
    path('suggest/',views.suggestion,name='suggestion'),
    path('suggest/suggestPhone',views.suggestphone,name='suggestphone'),
    # path('user/<int:pk>',views.Dashboard.as_view(),name='dashboard'),
    # path('user/getData/',views.getDashboard,name='getDashboard'),
    path('compare/getFeatures',views.getfeatures,name='getfeatures'),
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
    path('cart/',views.show_cart,name="showcart"),
    path('pluscart/',views.plus_cart,name='plus_cart'),
    path('minuscart/',views.minus_cart,name='minus_cart'),
    path('removecart/',views.remove_cart,name='remove_cart'),  
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('user/accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='userlogin'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('search/',views.searchbox,name='search'),
    path('delete/',views.delete,name='delete'),
    path('productviewcompare/<int:pk>',views.productviewcompare,name='productviewcompare'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),

    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),


    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),


    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),







    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
