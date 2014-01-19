from __future__ import unicode_literals
from __future__ import print_function

import urllib

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

import tvdbpy


class SeriesManager(models.Manager):

    def get_or_create(self, *args, **kwargs):
        extended = kwargs.pop('extended', False)

        instance, created = super(
            SeriesManager, self).get_or_create(*args, **kwargs)
        if created:
            instance.update_from_tvdb(extended=extended)

        return instance, created


class Series(models.Model):

    objects = SeriesManager()

    name = models.TextField()
    overview = models.TextField()
    first_aired = models.DateField(null=True)
    runtime = models.PositiveIntegerField(null=True)  # minutes
    network = models.TextField()
    tags = models.TextField()
    cast = models.TextField()
    poster = models.URLField()
    banner = models.URLField()
    completed = models.BooleanField(default=False)
    tvdb_id = models.CharField(max_length=256)
    imdb_id = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'series'

    def __unicode__(self):
        return self.name

    def seasons(self, with_specials=False):
        episodes = self.episode_set
        if not with_specials:
            episodes = episodes.exclude(season=0)
        return episodes.distinct().values_list('season', flat=True)

    def episodes(self, with_specials=False):
        """Return a dictionary of seasons with a list of episodes."""

    @property
    def next_episode(self):
        episodes = self.episode_set.filter(
            first_aired__gt=datetime.utcnow()).order_by('first_aired')
        if episodes.exists():
            return episodes[0]

    @property
    def last_episode(self):
        episodes = self.episode_set.filter(
            first_aired__lte=datetime.utcnow()).order_by('-first_aired')
        if episodes.exists():
            return episodes[0]

    def update_from_tvdb(self, extended=True):
        """Update this instance using the remote info from TvDB site."""
        client = tvdbpy.TvDB(settings.TVDBPY_API_KEY)
        tvdb_series = client.get_series_by_id(
            self.tvdb_id, full_record=extended)
        attrs = (
            'name', 'overview', 'first_aired', 'runtime',  'network',
            'poster', 'banner', 'imdb_id',
        )
        for attr in attrs:
            setattr(self, attr, getattr(tvdb_series, attr))

        self.cast = ', '.join(tvdb_series.actors)
        self.tags = ', '.join(tvdb_series.genre)

        self.completed = (tvdb_series.status.lower() == 'ended')

        if extended:
            # load seasons, which are already fetched
            self._fetch_episodes(tvdb_series)

        self.save()

    def _fetch_episodes(self, tvdb_series):
        for season, episodes in tvdb_series.seasons.iteritems():
            for i, e in episodes.iteritems():
                episode, _ = Episode.objects.get_or_create(
                    series=self, season=season, number=i, tvdb_id=e.id)
                episode.update_from_tvdb(e)


class Episode(models.Model):

    series = models.ForeignKey(Series)
    season = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    name = models.TextField()
    overview = models.TextField()
    first_aired = models.DateField(null=True)
    image = models.URLField()
    tvdb_id = models.CharField(max_length=256)
    imdb_id = models.CharField(max_length=256)
    guest_stars = models.TextField(null=True)
    writer = models.TextField(null=True)
    director = models.TextField(null=True)

    class Meta:
        unique_together = ('series', 'season', 'number')

    def __unicode__(self):
        return 'S%02dE%02d' % (self.season, self.number)

    def _blank_if_none(self, attr, value):
        if value is None:
            value = ''
        setattr(self, attr, value)

    def update_from_tvdb(self, tvdb_episode):
        attrs = (
            'director', 'image', 'name', 'overview', 'writer',
        )
        for attr in attrs:
            self._blank_if_none(attr, getattr(tvdb_episode, attr))
        self.first_aired = tvdb_episode.first_aired
        if tvdb_episode.guest_stars:
            self.guest_stars = ', '.join(tvdb_episode.guest_stars)
        self.save()

    @property
    def torrent_url(self):
        search_term = '%s %s' % (self.series.name, unicode(self))
        search_term = urllib.quote(search_term)
        return 'http://thepiratebay.se/search/%s/0/7/0' % search_term


class Watcher(models.Model):
    user = models.OneToOneField(User)
    series = models.ManyToManyField(Series)

    def series_from_yesterday(self):
        yesterday = datetime.utcnow().date() - timedelta(days=2)
        import pdb; pdb.set_trace()
        return self.series.filter(episode__first_aired=yesterday)

    def series_from_last_week(self):
        return []

    def series_for_next_week(self):
        return []



def create_watcher(sender, instance, created, raw, **kwargs):
    assert sender == User
    if created and not raw:
        Watcher.objects.create(user=instance)


models.signals.post_save.connect(
    create_watcher, sender=User, dispatch_uid='create_watcher_from_user')
