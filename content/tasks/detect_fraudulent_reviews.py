from datetime import datetime, timedelta

import pandas as pd
from sklearn.ensemble import IsolationForest
from celery import shared_task

from content.models import Review


@shared_task
def detect_fraudulent_reviews():
    end = datetime.now()
    start = end - timedelta(days=14)

    reviews = Review.objects.filter(
        created_at__gte=start,
        created_at__lte=end
    ).values('user', 'content', 'score', 'created_at')

    df = pd.DataFrame(reviews)
    df['created_at'] = df['created_at'].apply(lambda x: x.timestamp())
    features = df[['score', 'created_at']]

    model = IsolationForest(contamination=0.2)
    df['anomaly'] = model.fit_predict(features)

    anomalies = df[df['anomaly'] == -1]

    reviews_to_update = []
    for anomaly in anomalies.itertuples():
        review = Review(id=anomaly.id)
        review.is_fraud = True
        reviews_to_update.append(review)

    Review.objects.bulk_update(reviews_to_update, ['is_fraud'])
