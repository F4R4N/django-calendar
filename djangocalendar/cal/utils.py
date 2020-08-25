from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
from .models import Event
import jdatetime
from hijri_converter import convert

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        calendar.setfirstweekday(calendar.SATURDAY)
        
    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.get_html_url} </li>'
        
        if day != 0:
            jd = jdatetime.date.fromgregorian(day=day, month=self.month, year=self.year)
            hijri_date = convert.Gregorian(day=day, month=self.month, year=self.year).to_hijri()
            return f"<td title='{self.year}-{self.month}-{day} gregorian and {jd.year}-{jd.month}-{jd.day} shamsi and {hijri_date.year}-{hijri_date.month}-{hijri_date.day} ghamari' id='{self.year}-{self.month}-{day}'><span class='{day} date'>{day}</span><br><span class='{jd.day} jalali-day'>{jd.day}ش</span><br><span class='hijri-date {hijri_date.day}'>{hijri_date.day}ه</span><ul> {d} </ul></td>"
        return '<td></td>'
        
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'



    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal