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
    ).values('user_id', 'content_id', 'score', 'timestamp')

    df = pd.DataFrame(reviews)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    features = df[['score', 'hour']]

    model = IsolationForest(contamination=0.2)
    df['anomaly'] = model.fit_predict(features)

    anomalies = df[df['anomaly'] == -1]
    print(anomalies)

    for anomaly in anomalies.itertuples():
        review = Review.objects.get(id=anomaly.Index)
        review.is_fraud = True
        review.save()

    return

