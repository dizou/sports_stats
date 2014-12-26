__author__ = 'di'

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Max
from HTMLParser import HTMLParser


class Player(models.Model):
    id_player = models.AutoField(primary_key=True)
    gid = models.IntegerField(null=False)
    espn_id = models.IntegerField(null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    espn_name = models.CharField(max_length=100, blank=False, null=False)
    team = models.CharField(max_length=50)

    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        db_table = u'player'
        app_label = 'sports_stats'


class Appearance(models.Model):
    id_appearance = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, null=False)
    gid = models.IntegerField(null=False)
    date = models.DateField(null=False)
    started = models.BooleanField(null=False, default=False)
    min = models.IntegerField(null=False, default=0)
    fg = models.IntegerField(null=False, default=0)
    fga = models.IntegerField(null=False, default=0)
    tp = models.IntegerField(null=False, default=0)
    tpa = models.IntegerField(null=False, default=0)
    ft = models.IntegerField(null=False, default=0)
    fta = models.IntegerField(null=False, default=0)
    orb = models.IntegerField(null=False, default=0)
    drb = models.IntegerField(null=False, default=0)
    rb = models.IntegerField(null=False, default=0)
    ast = models.IntegerField(null=False, default=0)
    stl = models.IntegerField(null=False, default=0)
    blk = models.IntegerField(null=False, default=0)
    to = models.IntegerField(null=False, default=0)
    pf = models.IntegerField(null=False, default=0)
    dq = models.IntegerField(null=False, default=0)
    plus_minus = models.IntegerField(null=False, default=0)
    dd = models.IntegerField(null=False, default=0)
    td = models.IntegerField(null=False, default=0)
    fanduel_pts = models.DecimalField(null=False, max_digits=6, decimal_places=2, blank=True)
    draftkings_pts = models.DecimalField(null=False, max_digits=6, decimal_places=2, blank=True)
    draftday_pts = models.DecimalField(null=False, max_digits=6, decimal_places=2, blank=True)
    fanduel_position = models.IntegerField(null=False, default=0)
    fanduel_salary = models.IntegerField(null=False, default=0)
    draftkings_position = models.IntegerField(null=False, default=0)
    draftkings_salary = models.IntegerField(null=False, default=0)
    draftday_position = models.IntegerField(null=False, default=-1)
    draftday_salary = models.IntegerField(null=False, default=-1)
    team_pts = models.IntegerField(null=False, default=0)
    oppt_pts = models.IntegerField(null=False, default=0)
    total_pts = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = u'appearance'
        app_label = 'sports_stats'