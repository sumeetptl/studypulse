# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from .models import Topic, Room, Message
from .serializers import TopicSerializer, RoomSerializer, MessageSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TopicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        data = request.data
        data["host"] = request.user.id
        serializer = self.serializer_class(data=data)
        # serializer = RoomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors
            }, status=422)
        serializer.save()
        return Response({
            "message": "Room created Successfully",
            "room": serializer.data
        }, status=201)


class RoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def post(self, request, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = self.serializer_class(data=data)
        # serializer = RoomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors
            }, status=422)
        serializer.save()
        return Response({
            "message": "Message created Successfully",
            "room": serializer.data
        }, status=201)
