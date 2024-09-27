from django.contrib import admin

from .models import (
    Faculty, Gallery, Course, Message, Batch, Alumni, Tag, PopUp, IpHash,Event
)

admin.site.register([
    Faculty, Gallery, Course, Message,
    Batch, Alumni, Tag, PopUp, IpHash,Event
])

