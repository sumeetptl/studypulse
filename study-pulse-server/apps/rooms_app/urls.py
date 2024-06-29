from drf_spectacular import views
from django.urls import path
from .views import TopicListCreateAPIView, TopicRetrieveUpdateDestroyAPIView, \
    RoomListCreateAPIView, RoomRetrieveUpdateDestroyAPIView, \
    MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('schema/', views.SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('schema/swagger-ui/',
    #      views.SpectacularSwaggerView.as_view(url_name='schema'),
    #      name='swagger-ui'),
    path('topics/', TopicListCreateAPIView.as_view(),
         name='topic-list-create'),
    path('topics/<int:pk>/', TopicRetrieveUpdateDestroyAPIView.as_view(),
         name='topic-retrieve-update-destroy'),
    path('rooms/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomRetrieveUpdateDestroyAPIView.as_view(),
         name='room-retrieve-update-destroy'),
    path('messages/', MessageListCreateAPIView.as_view(),
         name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(),
         name='message-retrieve-update-destroy'),
]
