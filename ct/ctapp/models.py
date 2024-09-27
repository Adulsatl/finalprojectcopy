from datetime import datetime, timezone

from django.db import models


def time_now():
    return datetime.now(timezone.utc)

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="profile_pics/Faculty")
    link = models.CharField(max_length=100, null=True,
                            blank=True, help_text="Leave empty to auto create or add custom")
    designation = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()





class Tag(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    image = models.ImageField(upload_to="assets/images/Gallery")
    date = models.DateField(help_text="Images will be sorted on the basis of the dates.", null=True)
    tags = models.ManyToManyField(Tag, help_text="Select multiple tags related to the image", blank=True)
    description = models.CharField(max_length=30, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=50, null=True,
                            blank=True, help_text="Leave empty to auto create or add custom")
    description = models.TextField()
  

    def __str__(self):
        return self.name




class Message(models.Model):
    author = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(help_text="Messages will be sorted on basis of this date")
    content = models.TextField()


class IpHash(models.Model):
    hash = models.CharField(max_length=10, primary_key=True)
    visit_time = models.DateTimeField(default=time_now)

    class Meta:
        verbose_name = "Site Visitor"

    def __str__(self):
        return f"Visited on {self.visit_time.date()} at {self.visit_time.time()}"


class PopUp(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True, help_text="Optional")
    description = models.TextField(null=True, blank=True, help_text="Optional")
    image = models.ImageField(upload_to="assets/images/popups")
    
    def __str__(self):
        return self.title

class Batch(models.Model):
    year = models.DateField()

    def __str__(self):
        return str(self.year.year)

    @property
    def has_images(self):
        return self.alumni.first()


class Alumni(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="alumni")
    image = models.ImageField(upload_to="assets/images/alumni")

class Event(models.Model):
    name = models.CharField(max_length=100)
    link = models.SlugField(max_length=30, null=True,
                            blank=True, help_text="Leave empty to auto create or add custom",
                            unique=True)
    registration_open_date = models.DateTimeField(null=True)
    registration_end_date = models.DateTimeField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    image = models.ImageField(upload_to="assets/images/popups")
    # venue = models.CharField(max_length=30)
    # topic = models.CharField(max_length=30, null=True, blank=True)
    # host = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField()
    # markdown_content = models.TextField(null=True, blank=True, help_text="Markdown content if any")
    # staff_in_charge = models.ForeignKey("ctapp.Faculty", on_delete=models.SET_NULL, null=True, blank=True)
    # registration_link = models.URLField(null=True, blank=True, help_text="Optional")
    special_message = models.TextField(null=True, blank=True, help_text="Special message to send in email if any")
    # listing_order = models.IntegerField(default=0)



    @property
    def status(self):
        if time_now() < self.start_date:
            return "upcoming"
        elif time_now() > self.end_date:
           return "ended"
        return "live"

    @property
    def month(self):
        return self.start_date.strftime('%B')[:3]

    @property
    def short_description(self):
        if len(self.description) <= 120:
            return self.description

        short_content = self.description[:120]
        rightmost_space = short_content.rfind(" ")
        rightmost_newline = short_content.rfind("\n")
        rightmost_separator = max((rightmost_space, rightmost_newline))
        return short_content[:rightmost_separator]

def __str__(self):
    return self