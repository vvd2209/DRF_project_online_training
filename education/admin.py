from django.contrib import admin

from education.models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'course', 'owner',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('course', 'payment_date', 'amount', 'pay_type',)