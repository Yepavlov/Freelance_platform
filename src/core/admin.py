from django.contrib import admin

from core.models import City, Country, Skill, State

admin.site.register(
    [
        City,
        State,
        Country,
        Skill,
    ]
)
