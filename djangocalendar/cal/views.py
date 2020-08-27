from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from django.urls import reverse
from .forms import EventForm, SearchForm
from .models import *
from .utils import Calendar
import jdatetime
from hijri_converter import convert
class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        latest_events = Event.objects.order_by('-created')[:4]
        
        
        # mil_year = int(convert.datetime.datetime.now().strftime('%Y'))
        # mil_month = int(convert.datetime.datetime.now().strftime('%m'))
        # mil_day = int(convert.datetime.datetime.now().strftime('%d'))
        # hij_date = convert.Gregorian(mil_year, mil_month, mil_day).to_hijri()
        
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['latest_events'] = latest_events
        context['year'] = datetime.today().year
        context['month'] = datetime.today().month
        context['day'] = datetime.today().day
        
        # context['jal_date'] = str(jdatetime.datetime.now().strftime('%B %Y'))
        # context['hij_date'] = hij_date.month_name() + ' ' + str(hij_date.year)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
    

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})
    
def event_search(request):
    form = SearchForm()
    query = None
    resaults = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            resaults = Event.objects.filter(title__contains=query) or Event.objects.filter(body__contains=query) or Event.objects.filter(author__contains=query)
    return render(request, 'cal/search.html', {'form': form, 'query': query, 'resaults': resaults})
