from django.contrib import admin

from .models import RatingCategory, Review

admin.site.register((RatingCategory, Review))
