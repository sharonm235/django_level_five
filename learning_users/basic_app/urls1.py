from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from basic_app import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'basic_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.RegisterView.as_view(),name='register'),
    # path('register/',views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="basic_app/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/',views.profile, name='profile'),
    # Add further urls and views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# # Old code
#
# from django.contrib import admin
# from django.urls import path
# from basic_app import views
# from django.conf import settings
# from django.conf.urls.static import static
#
# #TEMPLATE URLs
#
# app_name = 'basic_app'
#
# urlpatterns = [
#     path('',views.index,name='index'),
#     path('register',views.register,name='register'),
#     path('user_login',views.user_login,name='user_login'),
#     path('profile/',views.profile, name='profile'),
#     # Add further urls and views
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
