from django.http import Http404
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
# 1111111


def no_rest_no_model(request):
    gusets = [
        {
            "id": 1,
            "name": "rahim",
            "mobile": 2894656,
        },
        {
            "id": 2,
            "name": "mariem",
            "mobile": 545664,
        }
    ]
    return JsonResponse(gusets, safe=False)
# 222222


def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        "guests": list(data.values("name", "mobile"))
    }
    return JsonResponse(response)
# 3333333
# funcion based view


@api_view(["GET", "POST"])
def FBV_List(request):
    # Get
    if request.method == "GET":
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POSt
    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# 3333333.111111
# funcion based view


@api_view(["GET", "PUT", "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Get
    if request.method == "GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    # POSt
    elif request.method == "PUT":
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 4444444.1111
# class based view
# List and  create ==== GET and POST


class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
# 4444444.222222
# class based view
# GET-PUT-DELETE ===> class based view


class CBV_pk(APIView):
    def get_objct(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_objct(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_objct(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_objct(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#!!!!mixins
# 55555555..11111 mixis


class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
## get and post

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
# get and put and delete


class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


#!!generics********
# 6.1
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]


# 66....2 get put and delete

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
#!! 7-- viewsets****************


class viewsets_guests(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fieleds = ['movie']


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
#!!!---88888--- finde movie ----


@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
#!!---99------- creat new reservation ------


@api_view(['Post'])
def new_reservation(request):
    movies = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    gueset = Guest()
    gueset.name = request.data['name']
    gueset.mobile = request.data['mobile']
    gueset.save()
    reservation = Reservation()
    reservation.guest = gueset
    reservation.movie = movies
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)
