from rest_framework.permissions import IsAuthenticated
from movie.models import Movie
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import MovieModelSerializer
from .permissions import IsOwnerOrAdminOrReadOnly


class MovieAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    pagination_class = MovieAPIListPagination


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)