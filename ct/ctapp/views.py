import hashlib

from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404

from .models import Course, Faculty, Message, Gallery, Batch, Tag, IpHash,PopUp,Event
from django.views.generic import ListView, View
from utils.functions import generate_css_text_animation
from ipware import get_client_ip
from django.http import JsonResponse
from datetime import datetime

def dashboard_redirect(request):
    return redirect(to=settings)

# def IndexView(request):
#     faculties = Faculty.objects.all()
    

#     return render(request, 'index.html', {'faculties': faculties})



def about_view(request):
    return render(request, "about.html")

class IndexView(View):
    def get(self, request):
        context = {}

        # Fetch faculties from the database
        faculties = Faculty.objects.all()
        context["faculties"] = faculties
        # Fetch messages
        context["messages"] = Message.objects.all()
        # Get client IP and handle popups
        ip, is_routable = get_client_ip(request)
        if is_routable:
            ip_hash = hashlib.md5(str.encode(ip)).hexdigest()[:10]
            if not IpHash.objects.filter(hash=ip_hash).exists():
                IpHash.objects.create(
                    hash=ip_hash
                )
                PopUp = PopUp.objects.all()
                print(PopUp)
                context["popup"] = PopUp.objects.last()
                context["popup"] = PopUp.objects.all().order_by('-id')[1:]
                context["popup"] = PopUp.objects.all()

    
    
        return render(request, "index.html", context)

def faculty(request):
    faculty = Faculty.objects.all()  # Replace with your actual query
    # Assuming you have a faculty-lazyload.html template
    return render(request, "faculty.html", {"faculties": faculty})

def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculty_list.html', {'faculties': faculties})

def faculty_refresh(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculty_refresh.html', {'faculties': faculties})

class EventView(View):
    model = Event
    template_name = "event-details.html"

    def get(self, request, slug=None):
        if slug:
            try:
                event = self.model.objects.get(link=slug)
                return render(request, self.template_name, {"event": event})
            except self.model.DoesNotExist:
                return render(request, "404.html")
        else:
            events = Event.objects.all()
            return render(request, "events.html", {"events": events})


class CourseView(View):
    model = Course
    template_name = "course-details.html"

    def get(self, request, slug):
        try:
            course = self.model.objects.get(link=slug)
            return render(request, self.template_name, {"course": course})
        except self.model.DoesNotExist:
            return render(request, "404.html")


class GalleryListView(ListView):
    template_name = "gallery.html"
    model = Gallery
    paginate_by = 12
    queryset = model.objects.order_by('-date')
    extra_context = {"tags": Tag.objects.all()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = sorted(set([date[0].year for date in self.queryset.values_list('date')]), reverse=True)
        return context


class AlumniListView(ListView):
    template_name = "alumni.html"
    model = Batch
    paginate_by = 3
    queryset = Batch.objects.order_by('-year')


class TermsView(View):
    template_name = "terms.html"
    def get(self, request):
        return render(request, self.template_name)


class PrivacyView(View):
    template_name = "privacy.html"

    def get(self, request):
        return render(request, self.template_name)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

