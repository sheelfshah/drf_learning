from rest_framework import serializers
from .models import Country, State, CityTown, Person

# single country serializer
# other models have multiple serializers to facilitate
# creating the other features


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


class NestedCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CityTown
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'pincode',
            'is_city'
        ]


class StateAndCitySerializer(serializers.ModelSerializer):

    nested_cities = NestedCitySerializer(many=True)

    class Meta:
        model = State
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'nested_cities'
        ]


class CountrySerializer(serializers.ModelSerializer):

    states = serializers.SerializerMethodField()
    nested_states = StateAndCitySerializer(many=True, write_only=True)

    def get_states(self, obj):
        queryset = obj.states.all()
        request = self.context.get("request")
        return StateNameSerializer(queryset, many=True, context={'request': request}).data

    class Meta:
        model = Country
        fields = [
            'id', 'name',
            'description', 'population',
            'GDP', 'states',
            'nested_states'
        ]

    def create(self, validated_data):
        nested_states = validated_data.pop('nested_states')
        country = Country.objects.create(**validated_data)
        for state_json in nested_states:
            nested_cities = state_json.pop("nested_cities")
            state = State.objects.create(country=country, **state_json)
            for city_json in nested_cities:
                CityTown.objects.create(state=state, **city_json)
        return country

    def update(self, instance, validated_data):
        """
            No update is being performed as it is possible to modify the country,
            and all the states,but if the order in which
            the states and their cities is changed or if new states
            or cities are added, then it seems that there is no method to get the initial
            object and edit tthe necessary details.

            The only method I could come up with was to delete all states/cities and recreate
            them, but this will cause all the person objects to be deleted as well.

            If we are fine with setting the city field for a person as NULL, only then is
            this latter option feasible.

            Due to uncertainty, I decided to do no update at all.
        """
        return instance
