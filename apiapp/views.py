from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    CountrySerializer,
    StateSerializer,
    CityTownSerializer)

from .models import (
    Country, State,
    CityTown, Person)


class CountryList(APIView):
    serializer_class = CountrySerializer

    def get(self, request, format=None):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDetail(APIView):
    serializer_class = CountrySerializer

    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        country = self.get_object(pk)
        serializer = CountrySerializer(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        country = self.get_object(pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StateList(APIView):
    serializer_class = StateSerializer

    def get(self, request, format=None):
        states = State.objects.all()
        serializer = StateSerializer(
            states, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateDetail(APIView):
    serializer_class = StateSerializer

    def get_object(self, pk):
        try:
            return State.objects.get(pk=pk)
        except State.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        state = self.get_object(pk)
        serializer = StateSerializer(state, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        state = self.get_object(pk)
        serializer = StateSerializer(
            state, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        state = self.get_object(pk)
        state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityTownList(APIView):
    serializer_class = CityTownSerializer

    def get(self, request, format=None):
        cts = CityTown.objects.all()
        serializer = CityTownSerializer(
            cts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CityTownSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityTownDetail(APIView):
    serializer_class = CityTownSerializer

    def get_object(self, pk):
        try:
            return CityTown.objects.get(pk=pk)
        except CityTown.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ct = self.get_object(pk)
        serializer = CityTownSerializer(ct, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ct = self.get_object(pk)
        serializer = CityTownSerializer(
            ct, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ct = self.get_object(pk)
        ct.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
