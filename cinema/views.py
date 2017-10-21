from django.shortcuts import render
from .models import Film, Poster
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics, status
from cinema.serializers import UserSerializer, FilmSerializer, PosterSerializer, FilmListSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes
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


class FilmList(APIView):

    def get(self, request):
        film = Film.objects.all()
        serializer = FilmListSerializer(film, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)



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
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors)
        else:
            return HttpResponse(status=403)

    def get_object(self, id):
        try:
            return Film.objects.filter(id=id)[0]
        except Film.DoesNotExist:
            HttpResponse(status=404)

    def get(self, request, id):
        film = self.get_object(id)
        serializer = FilmSerializer(film, many=False)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, id):
        film = self.get_object(id)
        serializer = FilmSerializer(film, data=request.PUT)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        poster = self.get_object(id)
        poster.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class PosterList(APIView):

    @authentication_classes((JSONWebTokenAuthentication,))
    @permission_classes((IsAuthenticated, IsAdminUser))
    def post(self, request):
        print(request.FILES)
        try:
            film = Film.objects.filter(title=request.POST['title'], premiere_date=request.POST['premiere_date'])[0]
        except Film.DoesNotExist:
            return HttpResponse(status=404)
        Poster.objects.create(film=film, pic=request.FILES['file'])
        response_dict = {
            'message': 'Poster uploaded successfully!',
        }
        return JsonResponse(response_dict)

    def get(self, request, id):
        film = self.get_object(id)
        serializer = PosterSerializer(Poster.objects.filter(film=film), many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_object(self, id):
        try:
            return Poster.objects.filter(id=id)
        except Poster.DoesNotExist:
            HttpResponse(status=404)

    def put(self, request, id):
        poster = self.get_object(id)
        serializer = PosterSerializer(poster, data=request.PUT)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(serializer.errors)

    def delete(self, request, id):
        poster = self.get_object(id)
        poster.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)