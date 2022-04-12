from django.db import models

from course_api.utils.models.base import BaseModel
from course_api.users.models import User

class Board(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    
    def __str__(self):
        return self.title
class Status(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)

    def __str__(self):
        return self.title

class Task(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    board = models.ForeignKey(Board , on_delete=models.CASCADE , null=True,blank=True)
    status = models.ForeignKey(Status , on_delete=models.CASCADE , null=True,blank=True)

    def __str__(self):
        return self.title