# bookings/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Booking
from .forms import BookingForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def home(request):
    services = Service.objects.filter(active=True)
    return render(request, 'bookings/home.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, active=True)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to book a service.")
            return redirect('login')
        form = BookingForm(request.POST)
        if form.is_valid():
            scheduled_dt = form.cleaned_data['scheduled_at']
            tz = timezone.get_current_timezone()
            scheduled_dt = timezone.make_aware(scheduled_dt, timezone=tz)
            
            if scheduled_dt < timezone.now():
                form.add_error(None, "Selected time is in the past.")
            else:
                exists = Booking.objects.filter(
                    service=service, 
                    scheduled_at=scheduled_dt
                ).exclude(status=Booking.STATUS_CANCELLED).exists()
                
                if exists:
                    form.add_error(None, "This slot is already booked. Choose another time.")
                else:
                    booking = Booking.objects.create(
                        user=request.user,
                        service=service,
                        scheduled_at=scheduled_dt,
                        phone=form.cleaned_data.get('phone', ''),
                        notes=form.cleaned_data.get('notes', '')
                    )
                    messages.success(
                        request, 
                        f"Booking created for {service.name} on {scheduled_dt.strftime('%Y-%m-%d %H:%M')}."
                    )
                    return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/service_detail.html', {'service': service, 'form': form})

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-scheduled_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status not in [Booking.STATUS_CANCELLED, Booking.STATUS_COMPLETED]:
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.success(request, "Booking cancelled.")
    return redirect('my_bookings')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # auto-login after registration
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'bookings/register.html', {'form': form})

#gKUE[<@')

def service_list(request):
    services = Service.objects.filter(active=True)
    return render(request, 'bookings/service_list.html', {'services': services})


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

