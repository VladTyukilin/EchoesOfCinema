from movie.models import Movie

from rest_framework import viewsets
from .serializers import MovieModelSerializer
from .permissions import IsOwnerOrAdminOrReadOnly

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)