from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from basic_app import views


from django.conf import settings
from django.conf.urls.static import static


app_name = 'basic_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('order/',views.OrderView.as_view(),name='order'),
    path('register/',views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="basic_app/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('<username>/<int:pk>/', views.profile, name='profile'),
    path('objects/',views.ObjectListView.as_view(),name='object_list'),
    path('object/<int:pk>', views.ObjectDetailView.as_view(), name='object_detail'),
    path('object/new/', views.CreateObjectView.as_view(), name='object_new'),
    path('object/<int:pk>/edit/', views.ObjectUpdateView.as_view(), name='object_edit'),
    path('object/<int:pk>/remove/', views.ObjectDeleteView.as_view(), name='object_remove'),

    # Add further urls and views
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
