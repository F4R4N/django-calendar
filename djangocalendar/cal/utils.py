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
            hijri_date = convert.Gregorian(day=day, month=self.month, year=self.year).to_hijri()        
            jd = jdatetime.date.fromgregorian(day=day, month=self.month, year=self.year)
            
            jal_month = jdatetime.GregorianToJalali(self.year, self.month, 15)
            jal_month = jdatetime.datetime(jal_month.jyear, jal_month.jmonth, jal_month.jday).strftime(' | %B %Y')
            
            hij_month = convert.Gregorian(self.year, self.month, 15).to_hijri()
            hij_month = convert.Hijri(hij_month.year, hij_month.month, hij_month.day)
            
            
            return f"<span id='jal-month' style='display: none;'>{jal_month}</span><span id='hij-month' style='display:none;'> | {hij_month.month_name()} {hij_month.year}</span><td title='{self.year}-{self.month}-{day} gregorian and {jd.year}-{jd.month}-{jd.day} shamsi and {hijri_date.year}-{hijri_date.month}-{hijri_date.day} ghamari' id='{self.year}-{self.month}-{day}'><span class='{day} date'>{day}</span><br><span class='{jd.day} jalali-day'>{jd.day}ش</span><br><span class='hijri-date {hijri_date.day}'>{hijri_date.day}ه</span><ul> {d} </ul></td>"
        return '<td></td>'
        
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)
        # hij_date = convert.Gregorian(self.year, self.month, day).to_hijri()
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal