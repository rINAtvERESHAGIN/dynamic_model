from django.urls import path
from dynamo.views.DataLogging import DataLogging
from dynamo.views.Register import Register
# from dynamo.views import
from dynamo.views.RestoringObject import RestoringObject

urlpatterns = [
    path('<instance>/<app>/<model>/register', Register.as_view()),
    path('<instance>/<app>/<model>/log', DataLogging.as_view()),
    path('<instance>/<app>/<model>/restore', RestoringObject.as_view()),
]
