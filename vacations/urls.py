from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^history/$', views.VacationRequestHistoryListView.as_view(), name='request_history_list'),
    url(r'^create/$', views.VacationRequestCreate.as_view(), name='create'),
    url(r'^approve/$', views.TodoApproveListView.as_view(), name='todo_approve_list'),
    url(r'^all/$', views.TeamAllRequestListView.as_view(), name='team_all_request_list'),
    url(r'^(?P<request_id>\w+)/$', views.VacationRequestDetailView.as_view(), name='detail'),
]
