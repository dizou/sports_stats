__author__ = 'di'

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

try:
    from BeautifulSoup import BeautifulSoup
except:
    from bs4 import BeautifulSoup
import urllib2
import csv

from sports_stats.forms.data_forms import DateForm

data_url = "http://rotoguru1.com/cgi-bin/hoopstat-daterange.pl?startdate=%s&date=%s&saldate=%s&g=0&ha=&min=&tmptmin=0&tmptmax=999&opptmin=0&opptmax=999&gmptmin=0&gmptmax=999&gameday="


class IndexView(View):
    date_form = DateForm
    template_name = "index.html"

    def get(self, request):
        form = self.date_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.date_form(request.POST)
        if form.is_valid():
            date = str(form['date'].value()).replace('-', '')
            response = urllib2.urlopen(data_url % (date, date, date))
            html = response.read()
            soup = BeautifulSoup(html, 'html5lib')
            lines = str(soup.currentTag).split('\n')
            start_index = -1
            for i, line in enumerate(lines):
                if line.find('gid') < 0:
                    continue
                start_index = i
                break

            if start_index >= 0:
                lines = [line.replace('<br/>', '').replace('<br />', '').split(';') for line in lines[start_index:]]
                csv_response = HttpResponse(content_type='text/csv')
                csv_response['Content-Disposition'] = 'attachment; filename="%s.csv"' % date

                writer = csv.writer(csv_response)
                for line in lines:
                    writer.writerow(line)
                response = csv_response

            return response