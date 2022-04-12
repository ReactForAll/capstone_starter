from django.shortcuts import get_object_or_404, render

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, IntegerField
from rest_framework.exceptions import ValidationError
from course_api.tasks.models import Board, Status, Task
from rest_framework.permissions import IsAuthenticated

class BoardSerializer(ModelSerializer):    
    
    class Meta:
        model = Board
        exclude = ("created_by" , "external_id","deleted")

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        exclude = ("created_by" , "external_id","deleted")

class TaskSerializer(ModelSerializer):
    board_object = BoardSerializer(source="board", read_only=True)
    status_object = StatusSerializer(source="status" , read_only=True)
    status = IntegerField(required=True, write_only=True)
    class Meta:
        model = Task
        exclude = ( "external_id","deleted")

    def validate(self, attrs):

        validated_data =  super().validate(attrs)
        user = self.context["request"].user
        status = validated_data["status"]
        status_obj =  Status.objects.filter(created_by = user , id=status).first()
        if not status_obj:
            raise ValidationError({"status" : "not found"})
        validated_data["status"] = status_obj
        return validated_data


class BoardViewset(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by = self.request.user)

class StatusViewset(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by = self.request.user)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)

        board = get_object_or_404(Board.objects.filter(id=self.kwargs["boards_pk"] , created_by =self.request.user))
        return self.queryset.filter(board=board)

    def perform_create(self, serializer):
        board = get_object_or_404(Board.objects.filter(id=self.kwargs["boards_pk"] , created_by =self.request.user))
        serializer.save(board=board)