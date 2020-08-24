from django.db import models
from django.urls import reverse
from django.utils import timezone
class Event(models.Model):
    created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    body = models.TextField(max_length=100)
    time = models.TimeField()
    date = models.DateField()
    
    def __str__(self):
        return self.title
    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}" class="event-link" title="Description : {self.body}. AT : {self.time}, BY : {self.author}"> {self.title} </a>'
        
    def get_abs_url(self):
        return reverse('cal:event_edit', args={self.id})