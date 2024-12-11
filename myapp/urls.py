from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('crops', views.CropView, basename='crops')
urlpatterns = [
    path('api/', include(router.urls)),
    # path('register', views.register, name='register'),
    # path('', views.sign_in, name='login'),
    # path('logout', views.sign_out, name='logout'),
    path('', views.index, name='index'),
    path('results', views.results, name='results'),
    path('details',views.details, name='details'),
]
