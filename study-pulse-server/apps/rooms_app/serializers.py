from rest_framework import serializers
from apps.users_app.models import User
from .models import Topic, Room, Message


class TopicSerializer(serializers.ModelSerializer):
    rooms_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'rooms_count']

    def get_rooms_count(self, obj):
        return obj.rooms.count()


class RoomSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Room
        fields = ['id', 'name', 'description',
                  'created', 'updated', 'topic', 'host']

    def create(self, validated_data):
        try:
            topic_data = validated_data.pop('topic')
            host_data = validated_data.pop('host')
            topic = Topic.objects.get(name=topic_data["name"])
            room = Room.objects.create(
                topic=topic, host=host_data, **validated_data)
            return room
        except Topic.DoesNotExist as e:
            raise serializers.ValidationError(
                e.errors, "Please choose right topic")


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'user', 'room', "body", "created", "updated"]

    def create(self, validated_data):
        try:
            room = validated_data.pop('room')
            user = validated_data.pop('user')
            message = Message.objects.create(
                room=room, user=user, **validated_data)
            return message
        except Topic.DoesNotExist as e:
            raise serializers.ValidationError(
                e.errors, "Please choose right topic")
