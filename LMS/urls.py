
from django.contrib import admin
from django.urls import path, include
from .import views, user_login
from django.conf import settings
from .views import  success_page, cancel_page
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('theboss', admin.site.urls),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('base', views.BASE, name='base'),
    path('404', views.PAGE_NOT_FOUND, name='404'),
    path('', views.HOME, name='home'),
    path('courses', views.SINGLE_COURSE, name='single_course'),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),
    path('search',views.SEARCH_COURSE, name ='search_course'),
    path('contact', views.CONTACT_US, name='contact_us'),
    path('about', views.ABOUT_US, name='about_us'),
    path('accounts/register', user_login.REGISTER, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin', user_login.DO_LOGIN, name='doLogin'),
    path('accounts/profile', user_login.PROFILE, name='profile'),
    path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),
    path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),
    path('my-course', views.MY_COURSE, name='my_course'),
    # path('checkout/<str:id>', checkout, name='checkout'),
    path('cancel', cancel_page, name='cancel'),
    path('success/<str:slug>', success_page, name='success'),
    path('course/watch-course/<slug:slug>', views.WATCH_COURSE, name='watch_course'),
    # path('subscribe', views.subscribe, name='subscribe'),
    # path('newsletter', views.newsletter, name='newsletter'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail')



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     ]
# urlpatterns += i18n_patterns (
#
#
#     path('ckeditor/', include('ckeditor_uploader.urls')),
#
#     path('base', views.BASE, name='base'),
#     path('404', views.PAGE_NOT_FOUND, name='404'),
#     path('', views.HOME, name='home'),
#     path('courses', views.SINGLE_COURSE, name='single_course'),
#     path('courses/filter-data',views.filter_data,name="filter-data"),
#     path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),
#     path('search',views.SEARCH_COURSE, name ='search_course'),
#     path('contact', views.CONTACT_US, name='contact_us'),
#     path('about', views.ABOUT_US, name='about_us'),
#     path('accounts/register', user_login.REGISTER, name='register'),
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('doLogin', user_login.DO_LOGIN, name='doLogin'),
#     path('accounts/profile', user_login.PROFILE, name='profile'),
#     path('accounts/profile/update', user_login.PROFILE_UPDATE, name='profile_update'),
#     path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),
#     path('my-course', views.MY_COURSE, name='my_course'),
#     # path('checkout/<str:id>', checkout, name='checkout'),
#     path('cancel', cancel_page, name='cancel'),
#     path('success/<str:slug>', success_page, name='success'),
#     path('course/watch-course/<slug:slug>', views.WATCH_COURSE, name='watch_course'),
#     path('subscribe', views.subscribe, name='subscribe'),
#     path('newsletter', views.newsletter, name='newsletter'),
#
#
#
#     prefix_default_language=False,
# ) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)