This is a Django REST Framework app with two models: study and assay. Each has a view and serializer.
The default sqlite database is used.
The rest_framework.pagination.PageNumberPagination class is used for pagination.

From a virtual environment, run

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The app will run on:
http://127.0.0.1:8000

Access a list of studies:
http://127.0.0.1:8000/api/studies/

Access a list of assays:
http://127.0.0.1:8000/api/assays/