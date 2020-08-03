from rest_framework import serializers
from .models import Country, State, CityTown, Person


class CountrySerializer(serializers.ModelSerializer):

    states = serializers.SerializerMethodField()

    def get_states(self, obj):
        queryset = obj.states.all()
        request = self.context.get("request")
        return StateNameSerializer(queryset, many=True, context={'request': request}).data

    class Meta:
        model = Country
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'states'
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


class PersonSerializer(serializers.ModelSerializer):

    citytown = serializers.HyperlinkedRelatedField(
        queryset=CityTown.objects.all(), view_name='citytown-detail')

    class Meta:
        model = Person
        fields = [
            'id', 'name',
            'citytown'
        ]


class CityTownNameSerializer(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField(view_name="citytown-detail")

    class Meta:
        model = CityTown
        fields = [
            'name',
            'link'
        ]


class StateNameSerializer(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField(view_name="state-detail")
    citytowns = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = [
            'name',
            'link',
            'citytowns'
        ]

    def get_citytowns(self, obj):
        queryset = obj.citytowns.all()
        request = self.context.get("request")
        return CityTownNameSerializer(queryset, many=True, context={'request': request}).data
