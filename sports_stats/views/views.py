__author__ = 'di'

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from sports_stats.models import Player, Appearance

from bs4 import BeautifulSoup
import urllib2
import csv

from sports_stats.forms.data_forms import DateForm

data_url = "http://rotoguru1.com/cgi-bin/hoopstat-daterange.pl?startdate=%s&date=%s&saldate=%s&g=0&ha=&min=&tmptmin=0&tmptmax=999&opptmin=0&opptmax=999&gmptmin=0&gmptmax=999&gameday="


def num_or_none(val, num_func, default=0):
    if val == '':
        return default
    try:
        return num_func(val)
    except:
        raise


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

                existing_appearance_ids = set([(int(a['gid']), str(a['date']).replace('-', '')) for a in Appearance.objects.values('gid', 'date')])
                appearance_ids = set([(int(line[0]), date) for line in lines if line[0].isdigit()])
                new_appearance_ids = appearance_ids - existing_appearance_ids

                player_ids = set([int(line[0]) for line in lines if line[0].isdigit()])
                existing_player_ids = set([int(p['gid']) for p in Player.objects.values('gid')])
                new_player_ids = player_ids - existing_player_ids

                new_players = []
                new_appearances = []
                fields = lines[0]
                for line in lines[1:]:
                    gid = line[0]
                    if gid.isdigit():
                        if int(gid) in new_player_ids:
                            new_players.append(
                                Player(
                                    gid=gid,
                                    last_name=line[1][:line[1].find(',')],
                                    first_name=line[1][line[1].find(',') + 2:],
                                    espn_id=line[2],
                                    espn_name=line[3],
                                    team=line[4]
                                )
                            )

                Player.objects.bulk_create(new_players)

                for line in lines[1:]:
                    gid = line[0]
                    if gid.isdigit():
                        if (int(gid), date) in new_appearance_ids:
                            new_appearances.append(
                                Appearance(
                                    player=Player.objects.get(gid=gid),
                                    gid=gid,
                                    date=date[0:4] + '-' + date[4:6] + '-' + date[6:],
                                    started=num_or_none(line[6], int),
                                    min=num_or_none(line[7], int),
                                    fg=num_or_none(line[8], int),
                                    fga=num_or_none(line[9], int),
                                    tp=num_or_none(line[10], int),
                                    tpa=num_or_none(line[11], int),
                                    ft=num_or_none(line[12], int),
                                    fta=num_or_none(line[13], int),
                                    orb=num_or_none(line[14], int),
                                    drb=num_or_none(line[15], int),
                                    rb=num_or_none(line[16], int),
                                    ast=num_or_none(line[17], int),
                                    stl=num_or_none(line[18], int),
                                    blk=num_or_none(line[19], int),
                                    to=num_or_none(line[20], int),
                                    pf=num_or_none(line[21], int),
                                    dq=num_or_none(line[22], int),
                                    plus_minus=num_or_none(line[23], int),
                                    dd=num_or_none(line[24], int),
                                    td=num_or_none(line[25], int),
                                    fanduel_pts=num_or_none(line[26], float),
                                    draftkings_pts=num_or_none(line[27], float),
                                    draftday_pts=num_or_none(line[28], float),
                                    fanduel_position=num_or_none(line[29], int),
                                    fanduel_salary=num_or_none(line[30], int),
                                    draftkings_position=num_or_none(line[31], int),
                                    draftkings_salary=num_or_none(line[32], int),
                                    draftday_position=num_or_none(line[33], int, -1),
                                    draftday_salary=num_or_none(line[34], int, -1),
                                    team_pts=num_or_none(line[35], int),
                                    oppt_pts=num_or_none(line[36], int),
                                    total_pts=num_or_none(line[37], int),
                                )
                            )

                Appearance.objects.bulk_create(new_appearances)

            return response