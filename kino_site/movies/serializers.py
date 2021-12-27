from rest_framework import serializers
from .models import Movie, Review, Rating
import gc


class MovieListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")

class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent = None)
        return super().to_representation(data)

class RecurciveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        # print(self.parent.__class__)
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""
    children = RecurciveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзывов"""

    class Meta:
        model = Review
        fields = "__all__"

class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip = validated_data.get('ip', None),
            movie = validated_data.get('movie', None),
            defaults = {'star': validated_data.get("star")}
        )
        return rating

class MovieDetailSerializer(serializers.ModelSerializer):
    #slug_field - чтобы выводилось поле в категории ввиде названия вместо id
    #read_only - поле только для чтения
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many = True)
    class Meta:
        model = Movie
        #exclude - для вывода всех полей за исключением ...
        exclude = ("draft", )