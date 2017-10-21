from django.conf.urls import include, url
from django.views.generic import TemplateView
#from cinema.views import UserListAPIView, film_list, index, film_detail
from cinema.views import index, UserListAPIView, admin_check, reg_form, FilmDetail, PosterList
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token


urlpatterns = [
    url(r'api/v1/auth/login/', obtain_jwt_token),
    url(r'api-token-verify/', verify_jwt_token),
    url(r'users/', UserListAPIView.as_view()),
    url(r'admin_check/', admin_check),
    url(r'reg_form/', reg_form),
    url(r'film/', FilmDetail.as_view()),
    url(r'poster/(?P<id>[0-9]+)/', PosterList.as_view()),
    url(r'poster', PosterList.as_view(), name='poster'),
    url(r'^.*$', index),
    #url(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
