from django.db import models
from django.core.validators import MaxValueValidator


class Content(models.Model):
    title = models.CharField(max_length=64, unique=True)
    context = models.CharField(max_length=128)
    average_score = models.FloatField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    user = models.CharField(max_length=20)
    score = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5),
        ]
    )
    is_fraud = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return f'{self.content}: {self.score}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            old_score = 0
        else:
            old_review = Review.objects.get(pk=self.pk)
            old_score = old_review.score

        total_score = self.content.average_score * self.content.reviews_count
        if is_new:
            self.content.reviews_count += 1
        else:
            total_score -= old_score

        total_score += self.score
        self.content.average_score = total_score / self.content.reviews_count

        self.content.save()

        super().save(*args, **kwargs)

    class Meta:
        unique_together = [['user', 'content']]
