from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar
from .models import Event
import jdatetime


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()
        calendar.setfirstweekday(calendar.SATURDAY)
	# formats a day as a td
	# filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.get_html_url} </li>'
        jd = jdatetime.date.fromgregorian(day=day, month=self.month, year=self.year)
        if day != 0:
            return f"<td class='{day}'><span class='{day} date'>{day}</span><br><span class='{jd.day} jalali-day'>{jd.day}</span><ul> {d} </ul></td>"
        return '<td></td>'
        
    


	# formats a week as a tr 
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal