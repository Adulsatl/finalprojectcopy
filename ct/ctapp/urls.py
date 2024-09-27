from django.urls import path
from .views import (
    IndexView, about_view, GalleryListView,
    EventView, CourseView, AlumniListView,
    PrivacyView, TermsView,faculty,faculty_list,faculty_refresh
)

from django.conf import settings

from django.conf.urls.static import static
from django.urls import path

from .views import custom_404

app_name = "ctapp"
handler404 = custom_404

urlpatterns = [
    path('', IndexView.as_view(), name="Home"),
    path('eventsd/', EventView.as_view(), name="event_details"),
    path('events/', EventView.as_view(), name="events"),
    path('about/', about_view, name="about"),
    path('gallery/', GalleryListView.as_view(), name="gallery"),
    path('alumni/', AlumniListView.as_view(), name="alumni"),
    path('privacy/', PrivacyView.as_view(), name="privacy"),
    path('terms/', TermsView.as_view(), name="terms"),
    path('faculty/', faculty, name='faculty'),
    path('faculty_refresh/',faculty_refresh, name='faculty_refresh'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
