# Bitpin

Bitpin is a Django application for managing content reviews.

## Prerequisites

Before running Bitpin, ensure you have the following installed:

- PostgreSQL
- Redis

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ali-alef/bit-pin
   cd bitpin
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
   - Create a database named `bitpin` in PostgreSQL.
   - Configure your `DATABASES` setting in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'bitpin',
             'USER': 'user',
             'PASSWORD': 'password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. Set up Redis:
   - Ensure Redis is running and accessible.
   - Configure Celery settings in `settings.py` for shared tasks:
     ```python
     CELERY_BROKER_URL = 'redis://localhost:6379/0'
     CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
     ```

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

To use Bitpin, follow these steps:

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. bitpin service is now running at `http://localhost:8000`.

## Models

### Content

Represents a piece of content with associated reviews.

- **Fields:**
  - `title`
  - `context`
  - `average_score`
  - `reviews_count`

### Review

Represents a review of a specific content.

- **Fields:**
  - `user`
  - `score`
  - `is_fraud`
  - `created_at`
  - `content`

- **Custom Save Method:**
  - Calculates and updates `average_score` and `reviews_count` of associated `Content` when saving a `Review`.

## Automated Task

### Detect Fraudulent Reviews

Automatically detects and marks potentially fraudulent reviews using an Isolation Forest model. This task runs periodically to identify anomalies in recent review data.

#### How It Works

1. Fetches reviews created within the last 14 days.
2. Converts review data into a Pandas DataFrame.
3. Applies Isolation Forest algorithm to detect anomalies (potentially fraudulent reviews).
4. Updates `is_fraud` field for detected anomalies in bulk using Django's `bulk_update` method.

#### Implementation

The `detect_fraudulent_reviews` task is implemented as a Celery shared task.

## Testing Endpoints

You can test the endpoints using CURL commands:

### List of Contents

Fetches a list of contents. If `user` is provided in the query parameter, it shows the user's review on each content if it exists.

```bash
curl --location 'localhost:8000/contents/?user=user'
```

### Create Content

Creates a new content.

```bash
curl --location 'localhost:8000/contents/' \
--header 'Content-Type: application/json' \
--data '{
    "title": "test_2",
    "context": "This is second test for creating content"
}'
```

### Create or Update Review

Creates or updates a review. If a record with the requested user and content ID already exists, it updates the review.

```bash
curl --location 'localhost:8000/reviews/' \
--header 'Content-Type: application/json' \
--data '{
    "user": "user",
    "score": 3,
    "content": 1
}'
```
---
