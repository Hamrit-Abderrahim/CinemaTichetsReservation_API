
from django import urls, views
from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("guests", views.viewsets_guests)
router.register("movie", views.viewsets_movie)
router.register("reservtion", views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    #!!!!----- 1 ------
    # 111111
    path('django/jsonresponsenomdel/', views.no_rest_no_model),
    #!!!!----- 2 ------
    # 222222
    path('django/jsonresponsefrommodel/', views.no_rest_from_model),
    #!!!!----- 3 ------
    # 333333
    path('rest/fbv/', views.FBV_List),
    # 333333.11111
    path('rest/fbv/<int:pk>', views.FBV_pk),
    #!!!!----- 4 ------
    # 4444444.11111
    path('rest/cbv/', views.CBV_List.as_view()),
    # 4444444.222
    path('rest/cbv/<int:pk>', views.CBV_pk.as_view()),
    #!!!!----- 5 ------
    # 555.111111
    path('rest/mixins/', views.mixins_list.as_view()),
    # 555.222222
    path('rest/mixins/<int:pk>', views.mixins_pk.as_view()),
    #!!!!----- 6 ------
    # 666.111111
    path('rest/generics/', views.generics_list.as_view()),
    # 666.222222
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    #!!-- 7----
    path('rest/viewsets/', include(router.urls)),
    #!!-- 8----
    path('fbv/findmovie', views.find_movie),
    #!!-- 9 ----
    path('fbv/newreservation', views.new_reservation),
    #!!rest auth url
    path('api-auth', include('rest_framework.urls')),
    #!! Token Authentication
    path('api-token-auth', obtain_auth_token)
]
