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

                existing_appearance_ids = set([(int(a['gid']), a['date']) for a in Appearance.objects.values('player_id', 'date')])
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
                        if (gid, date) in new_appearance_ids:
                            new_appearances.append(
                                Appearance(
                                    player=Player.objects.get(gid=gid),
                                    date=date,
                                    started=line[6],
                                    min=line[7],
                                    fg=line[8],
                                    fga=line[9],
                                    tp=line[10],
                                    tpa=line[11],
                                    ft=line[12],
                                    fta=line[13],
                                    orb=line[14],
                                    drb=line[15],
                                    rb=line[16],
                                    ast=line[17],
                                    stl=line[18],
                                    blk=line[19],
                                    to=line[20],
                                    pf=line[21],
                                    dq=line[22],
                                    plus_minus=line[23],
                                    dd=line[24],
                                    td=line[25],
                                    fanduel_pts=line[26],
                                    draftkings_pts=line[27],
                                    draftday_pts=line[28],
                                    fanduel_position=line[29],
                                    fanduel_salary=line[30],
                                    draftkings_position=line[31],
                                    draftkings_salary=line[32],
                                    draftday_position=line[33],
                                    draftday_salary=line[34],
                                    team_pts=line[35],
                                    oppt_pts=line[36],
                                    total_pts=line[37],
                                )
                            )
                Appearance.objects.bulk_create(new_appearances)

            return response