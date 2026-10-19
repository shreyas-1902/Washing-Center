# bookings/admin.py
from django.contrib import admin
from .models import Service, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'scheduled_at', 'status', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('user__username', 'user__email', 'service__name')
    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed']

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_CONFIRMED)
        self.message_user(request, f"{updated} bookings marked as confirmed.")
    mark_confirmed.short_description = "Mark selected bookings as Confirmed"

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_CANCELLED)
        self.message_user(request, f"{updated} bookings marked as cancelled.")
    mark_cancelled.short_description = "Mark selected bookings as Cancelled"

    def mark_completed(self, request, queryset):
        updated = queryset.update(status=Booking.STATUS_COMPLETED)
        self.message_user(request, f"{updated} bookings marked as completed.")
    mark_completed.short_description = "Mark selected bookings as Completed"
