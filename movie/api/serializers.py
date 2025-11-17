from rest_framework import serializers
from movie.models import Movie


class MovieModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'time_create', 'time_update', 'user')