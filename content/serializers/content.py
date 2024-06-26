from rest_framework import serializers
from content.models import Content, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'score', 'content']


class ContentSerializer(serializers.ModelSerializer):
    user_reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'context', 'average_score', 'reviews_count', 'user_reviews']
