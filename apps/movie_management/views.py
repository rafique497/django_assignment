"""
 view file
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
# django import
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.accounts.message import ERROR_CODE, SUCCESS_CODE
from apps.movie_management.filter import MovieListFilter
from apps.movie_management.models import Movie, Review
from apps.movie_management.pagination import return_paginated_response
from apps.movie_management.serializer import MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer
from apps.movie_management.utils import CollaborativeFiltering


class MovieViewSet(GenericViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filterset_class = MovieListFilter

    def list(self, request, *args, **kwargs):
        return return_paginated_response(self.serializer_class, request,
                                         self.filter_queryset(self.get_queryset()))

    def retrieve(self, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        if instance is not None:
            serializer = MovieWithReviewsSerializer(instance)
            return Response({'data': serializer.data})
        return Response({'message': ERROR_CODE['4003']})


class ReviewViewSet(GenericViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def list(self, request, *args, **kwargs):
        return return_paginated_response(self.serializer_class, request,
                                         self.filter_queryset(self.get_queryset()))

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': SUCCESS_CODE['2001']})
        return Response({'message': ERROR_CODE['4004']})

    def retrieve(self, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        if instance is not None:
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data})
        return Response({'message': ERROR_CODE['4003']})

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        if instance is not None:
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data})
            return Response({'message': ERROR_CODE['4004']})
        return Response({'message': ERROR_CODE['4003']})

    def destroy(self, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        if instance is not None:
            instance.delete()
            return Response({'data': SUCCESS_CODE['2003']})
        return Response({'message': ERROR_CODE['4003']})

    @action(methods=['get'], url_path='user-review', url_name='user-review',
            detail=True)
    def user_review_list(self, request, *args, **kwargs):
        user_reviews = self.get_queryset().filter(user__id=kwargs.get('pk'))
        serializer = self.get_serializer(user_reviews, many=True)
        return Response({'reviews': serializer.data})

    @action(detail=True, methods=['get'], url_path='recommendation', url_name='recommendation')
    def recommend_movies(self, request, *args, **kwargs):
        ratings_data = Review.objects.filter(user__id=kwargs['pk']).values('user', 'movie', 'rating')
        data_list = [(item['user'], item['movie'], item['rating']) for item in ratings_data]
        cf = CollaborativeFiltering(num_users=100, num_movies=1000)
        cf.train(data_list)
        top_n = request.query_params.get('top_n', 10)
        try:
            top_n = int(top_n)
        except ValueError:
            return Response({'error': 'Invalid value for top_n'}, status=status.HTTP_400_BAD_REQUEST)

        recommendations = cf.recommend_movies(kwargs['pk'], top_n)
        return Response({'recommendations': recommendations}, status=status.HTTP_200_OK)

