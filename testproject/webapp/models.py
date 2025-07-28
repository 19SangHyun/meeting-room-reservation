from django.contrib.auth.models import AbstractUser
from django.db import models

# 사용자 모델
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# 회의실 모델
class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# 예약 모델
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name} 예약 - {self.date} {self.start_time}~{self.end_time}"

    class Meta:
        unique_together = ('room', 'date', 'start_time', 'end_time')  # 중복 예약 방지

