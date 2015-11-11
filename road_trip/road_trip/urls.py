"""road_trip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers
from trip.views import TripViewSet, CityViewSet, ActivityViewSet, \
                       suggestion_json, selection_json, interests_json, \
                       user_create, logout, trip_save, get_trips, who_am_i

router = routers.DefaultRouter()
router.register(r'trip', TripViewSet)

trip_router = routers.NestedSimpleRouter(router, r'trip', lookup='trip')
trip_router.register(r'city', CityViewSet)

activity_router = routers.NestedSimpleRouter(trip_router, r'city', lookup='city')
activity_router.register(r'activity', ActivityViewSet)

# trip_router.register(r'suggestions', suggestion_json)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'api/trip/(?P<trip_pk>\d+)/suggestions/', suggestion_json),
    url(r'api/trip/(?P<trip_pk>\d+)/selections/', selection_json),
    url(r'api/trip/(?P<trip_pk>\d+)/interests/', interests_json),
    url(r'api/trip/(?P<trip_pk>\d+)/save/', trip_save),
    url(r'api/trips/', get_trips),
    url(r'api/', include(router.urls)),
    url(r'api/', include(trip_router.urls)),
    url(r'api/', include(activity_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/login/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^api/register/', user_create),
    url(r'^api/logout/', logout),
    url(r'^api/whoami/', who_am_i)

]
