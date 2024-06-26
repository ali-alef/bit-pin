from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.response import Response
from content.models import Content, Review
from content.serializers import ContentSerializer, ReviewSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.query_params.get('user', None)

        queryset = self.get_queryset()

        if user:
            queryset = queryset.prefetch_related(
                Prefetch('reviews', queryset=Review.objects.filter(user=user), to_attr='user_reviews')
            )
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request):
        data = request.data
        user = data.get('user', None)
        content = data.get('content', None)

        review = Review.objects.filter(user=user, content=content)

        if review.exists():
            serializer = ReviewSerializer(review.last(), data=request.data)
        else:
            serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK if review.exists() else status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)