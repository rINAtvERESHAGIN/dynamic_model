from django.urls import path
from dynamo.views.DataLogging import DataLogging
from dynamo.views.Register import Register
# from dynamo.views import
from dynamo.views.RestoringObject import RestoringObject
from web.views.GetAllAction import AllActionData
from web.views.GetTableName import GetTableName
from web.views.GetTableName import SendDynamicData
from web.views import views
from web.views import cards
urlpatterns = [
    path('getTableName/', GetTableName.as_view()),
    path('getDynamicTableData/', SendDynamicData.as_view()),
    path('getAllAction/', views.get_all_action),
    path('getCardsData/', cards.get_cards_info),
]
