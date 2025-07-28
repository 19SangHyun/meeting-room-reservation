# webapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import SignUpForm
from .models import Room
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from django.utils.timezone import localdate
from .models import Reservation
from django.core.serializers.json import DjangoJSONEncoder
import json


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'webapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('room_list')  # 로그인 후 회의실 목록 페이지로 이동
        else:
            return render(request, 'webapp/login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})

    return render(request, 'webapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'webapp/room_list.html', {'rooms': rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    today = localdate()
    # 오늘 이후 예약만 보여주기 (원한다면 기간 조정 가능)
    reservations = Reservation.objects.filter(room=room, date__gte=today).order_by('date', 'start_time')
    context = {
        'room': room,
        'reservations': reservations,
    }
    return render(request, 'webapp/room_detail.html', context)

@login_required
def make_reservation(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    today = localdate()
    existing_reservations = Reservation.objects.filter(room=room, date__gte=today).order_by('date', 'start_time')

    # 예약된 시간 리스트를 JSON 형태로 변환 (프론트에서 사용)
    reservations_json = json.dumps([
        {
            'date': r.date.strftime('%Y-%m-%d'),
            'start_time': r.start_time.strftime('%H:%M'),
            'end_time': r.end_time.strftime('%H:%M'),
        } for r in existing_reservations
    ], cls=DjangoJSONEncoder)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            new_date = form.cleaned_data['date']
            new_start = form.cleaned_data['start_time']
            new_end = form.cleaned_data['end_time']

            overlapping = Reservation.objects.filter(
                room=room,
                date=new_date,
                start_time__lt=new_end,
                end_time__gt=new_start
            ).exists()

            if overlapping:
                form.add_error(None, '해당 시간에 이미 예약이 있습니다.')
            else:
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.room = room
                reservation.save()
                return redirect('room_detail', room_id=room.id)
    else:
        form = ReservationForm()

    return render(request, 'webapp/make_reservation.html', {
        'form': form,
        'room': room,
        'existing_reservations': reservations_json,
    })