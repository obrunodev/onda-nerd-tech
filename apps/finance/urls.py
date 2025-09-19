from apps.finance import views

from django.urls import path

app_name = 'finance'
urlpatterns = [
    path('create/', views.TransactionCreateView.as_view(), name='create'),
    path('', views.TransactionListView.as_view(), name='list'),
    path('<int:pk>/update/', views.TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle-status/',
         views.TransactionToggleStatusView.as_view(),
         name='toggle_status'),
]
