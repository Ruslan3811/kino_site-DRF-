from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Movie, Rating
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer

from .service import get_client_ip

from django.db import models

class MovieListView(APIView):
    def get(self, request):
        # movies = Movie.objects.filter(draft = False).annotate(
        #     rating_user=models.Case(
        #         models.When(ratings__ip = get_client_ip(request), then=True),
        #         default = False,
        #         output_field= models.BooleanField()
        #     )
        # )
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user = models.Count(
                "ratings", filter=models.Q(
                    ratings__ip = get_client_ip(request)
                )
            )
        ).annotate(
            middle_star = models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')),
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(id = pk, draft = False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)

class ReviewCreateView(APIView):
    def post(self, request):
        #request.data - то что содержится в клиентском запросе
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)

class AddStarRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingSerializer(data = request.data)
        if (serializer.is_valid()):
            serializer.save(ip=get_client_ip(request))
            return Response(status = 201)
        else:
            return Response(status = 400)