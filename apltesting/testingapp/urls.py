from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('select', views.SelectionView.as_view(), name='select'),
    path('questions', views.QuestionsListView.as_view(), name='questions'),
    path('question/<pk>', views.QuestionUpdateView.as_view(), name='update-question'),
    path('entry/<site>', views.EntryView.as_view(), name='entry'),
    path('start/<test>', views.StartView.as_view(), name='start'),
    path('test', views.TestView.as_view(), name='test'),
    path('done', views.DoneView.as_view(), name='done'),
]
