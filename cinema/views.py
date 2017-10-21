from django.shortcuts import render
#from .models import Film
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics, status
from cinema.serializers import UserSerializer, FilmSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import jwt


# Create your views here.
def index(request):
    return render(request, 'index.html')

@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@authentication_classes((JSONWebTokenAuthentication, ))
@permission_classes((IsAuthenticated, IsAdminUser))
def admin_check(request):
    jwts = request.META['HTTP_AUTHORIZATION'][4:]
    jwt_decoded = jwt.decode(jwts, 'secret', algorithms=['HS256'], verify=False)
    curr_user = User.objects.filter(username=jwt_decoded['username'])[0]
    content = {
        'isAdmin': curr_user.is_staff  # `django.contrib.auth.User` instance.
    }
    if curr_user.is_staff:
        return JsonResponse(content)
    else:
        return HttpResponse(status=403)

@csrf_exempt
def reg_form(request):

    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors)


class FilmDetail(APIView):

    @authentication_classes((JSONWebTokenAuthentication,))
    @permission_classes((IsAuthenticated, IsAdminUser))
    def post(self, request):
        jwts = request.META['HTTP_AUTHORIZATION'][4:]
        jwt_decoded = jwt.decode(jwts, 'secret', algorithms=['HS256'], verify=False)
        curr_user = User.objects.filter(username=jwt_decoded['username'])[0]
        print(request.FILES)
        if curr_user.is_staff:
            serializer = FilmSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                print(serializer)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors)
        else:
            return HttpResponse(status=403)


class PosterList(APIView):

    @authentication_classes((JSONWebTokenAuthentication,))
    @permission_classes((IsAuthenticated, IsAdminUser))
    def post(self, request):
        print(request.FILES)
        print(request.POST)
        return HttpResponse(status=200)