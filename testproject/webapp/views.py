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
from django.core.exceptions import PermissionDenied
from django.contrib import messages


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

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.user != reservation.user and not request.user.is_staff:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            new_reservation = form.save(commit=False)

            # 중복 확인 (자기 자신 제외)
            overlapping = Reservation.objects.filter(
                room=reservation.room,
                date=new_reservation.date,
                start_time__lt=new_reservation.end_time,
                end_time__gt=new_reservation.start_time
            ).exclude(id=reservation.id)

            if overlapping.exists():
                form.add_error(None, '해당 시간에 이미 예약이 있습니다.')
            else:
                new_reservation.save()
                return redirect('room_detail', room_id=reservation.room.id)
    else:
        form = ReservationForm(instance=reservation)

    reservations = Reservation.objects.filter(room=reservation.room)

    return render(request, 'webapp/edit_reservation.html', {
        'form': form,
        'reservation': reservation,
        'reservations': reservations,
    })


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # 본인 또는 관리자만 삭제 가능
    if reservation.user != request.user and not request.user.is_staff:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('room_detail', room_id=reservation.room.id)

    if request.method == 'POST':
        room_id = reservation.room.id
        reservation.delete()
        messages.success(request, "예약이 삭제되었습니다.")
        return redirect('room_detail', room_id=room_id)

    return render(request, 'webapp/delete_reservation.html', {'reservation': reservation})