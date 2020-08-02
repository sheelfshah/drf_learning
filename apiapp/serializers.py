from rest_framework import serializers
from .models import Country, State, CityTown, Person


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP'
        ]

    def update(self, instance, validated_data):
        # name field is not editabele

        if 'name' in validated_data:
            del validated_data['name']
        return super().update(instance, validated_data)


class StateSerializer(serializers.ModelSerializer):

    country = serializers.HyperlinkedRelatedField(
        queryset=Country.objects.all(), view_name='country-detail')

    class Meta:
        model = State
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'country'
        ]

    def update(self, instance, validated_data):
        # name field is not editabele

        if 'name' in validated_data:
            del validated_data['name']
        return super().update(instance, validated_data)


class CityTownSerializer(serializers.ModelSerializer):

    state = serializers.HyperlinkedRelatedField(
        queryset=State.objects.all(), view_name='state-detail')

    class Meta:
        model = CityTown
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'pincode',
            'is_city', 'state'
        ]

    def update(self, instance, validated_data):
        # name field is not editabele

        if 'name' in validated_data:
            del validated_data['name']
        return super().update(instance, validated_data)
