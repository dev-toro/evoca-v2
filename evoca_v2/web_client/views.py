# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import render
from datetime import datetime
import collections

# Import models
from core.models import Channel, Record, Tag
from django.contrib.auth.models import User

class ChannelsListView(ListView):
    model = Channel
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super(ChannelsListView, self).get_context_data(**kwargs)
        return context

class RecordsListView(ListView):
    model = Record
    template_name = 'record_list.html'

    def orderQueryByDate(self, queryset):
        dates = []
        for s in queryset:
            _s = "" + str(s.created_at)
            k, v = _s.rsplit("-", 1)
            if(k not in dates):
                dates.append(k)
        response = collections.OrderedDict()
        iterator = iter(dates[::-1])
        for d in iterator:
            response[d] = queryset.filter(created_at__year=int(d[:4])).filter(created_at__month=int(d[5:])).order_by('created_at')
    	return response

    def getChannelUsers(self):
        queryset = Record.objects.all().filter(channel__slug=self.kwargs['channel'])
        response = []
        for s in queryset:
            user = User.objects.get(pk=s.author.pk).username
            if user not in response:
                response.append(user)
        return response

    def getChannelTags(self):
        queryset = Tag.objects.all().filter(related_channel__slug=self.kwargs['channel'])
        return queryset

    def getRecordsByTag(self):
        '''queryset = Tag.objects.all().filter(related_channel__slug=self.kwargs['channel'])
        response = []
        for s in queryset:
            tagName = s.slug
            listRecord = Record.objects.all().filter(channel__slug=self.kwargs['channel'])
            listTag = listRecord.filter(tags__in=s.slug)
            numTag = listTag.count()
            tagInfo = {'name' : s.name, 'count' : numTag}
            response.append(tagInfo)
        return response'''

    def get_queryset(self):
        queryset = super(RecordsListView, self).get_queryset().order_by('created_at').filter(channel__slug=self.kwargs['channel'])
        return self.orderQueryByDate(queryset)

    def get_context_data(self, **kwargs):
        context = super(RecordsListView, self).get_context_data(**kwargs)
        # Pass channel data to context
        context['active_channel_name'] = Channel.objects.get(slug=self.kwargs['channel']).name
        context['channel_users'] = self.getChannelUsers
        context['channel_tags'] = self.getChannelTags
        context['channel_tags_count'] = self.getRecordsByTag
        context['active_channel_slug'] = slug=self.kwargs['channel']
        context['filtered_by_user'] = "ninguno"
        context['filtered_by_tag'] = "ninguna"
        return context

class RecordsDetailView(DetailView):
    model = Record
    template_name = 'record_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RecordsDetailView, self).get_context_data(**kwargs)
        # Pass channel data to context
        context['active_channel_name'] = Channel.objects.get(slug=self.kwargs['channel']).name
        context['active_channel_slug'] = slug=self.kwargs['channel']
        return context


class RecordsStatsView(TemplateView):
    template_name = 'record_stats.html'

    def getChannelUsers(self):
        queryset = Record.objects.all().filter(channel__slug=self.kwargs['channel'])
        response = []
        for s in queryset:
            user = User.objects.get(pk=s.author.pk).username
            if user not in response:
                response.append(user)
        return len(response)

    def getChannelTags(self):
        queryset = Tag.objects.all().filter(related_channel__slug=self.kwargs['channel'])
        return len(queryset)

    def getChannelRecords(self):
        return Record.objects.all().filter(channel__slug=self.kwargs['channel']).count()

    def get_context_data(self, **kwargs):
        context = super(RecordsStatsView, self).get_context_data(**kwargs)
        # Pass channel data to context
        channel = Channel.objects.get(slug=self.kwargs['channel'])
        context['channel_records_count'] = self.getChannelRecords
        context['channel_users_count'] = self.getChannelUsers
        context['channel_users_count'] = self.getChannelUsers
        context['channel_tags_count'] = self.getChannelTags
        context['active_channel_name'] = channel.name
        context['active_channel_slug'] = slug=self.kwargs['channel']
        context['active_channel_ID'] = channel.uniqueID
        return context


class RecordsMapView(TemplateView):
    template_name = 'record_map.html'

    def getChannelUsers(self):
        queryset = Record.objects.all().filter(channel__slug=self.kwargs['channel'])
        response = []
        for s in queryset:
            user = User.objects.get(pk=s.author.pk).username
            if user not in response:
                response.append(user)
        return response

    def getChannelTags(self):
        queryset = Tag.objects.all().filter(related_channel__slug=self.kwargs['channel'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RecordsMapView, self).get_context_data(**kwargs)
        # Pass channel data to context
        channel = Channel.objects.get(slug=self.kwargs['channel'])
        context['channel_users'] = self.getChannelUsers
        context['channel_tags'] = self.getChannelTags
        context['active_channel_name'] = channel.name
        context['active_channel_slug'] = slug=self.kwargs['channel']
        context['active_channel_ID'] = channel.uniqueID
        context['filtered_by_user'] = "ninguno"
        context['filtered_by_tag'] = "ninguna"
        context['mapCenterLocation'] = channel.mapCenterLocation
        context['defaultZoom'] = channel.defaultZoom
        context['maxZoom'] = channel.maxZoom
        return context

class RecordsFilteredViewByUser(RecordsListView):
    def get_queryset(self):
        queryset = super(RecordsListView, self).get_queryset().order_by('created_at').filter(channel__slug=self.kwargs['channel']).filter(author__username=self.kwargs['user'])
        return self.orderQueryByDate(queryset)

    def get_context_data(self, **kwargs):
        context = super(RecordsListView, self).get_context_data(**kwargs)
        # Pass channel data to context
        context['active_channel_name'] = Channel.objects.get(slug=self.kwargs['channel']).name
        context['channel_users'] = self.getChannelUsers
        context['channel_tags'] = self.getChannelTags
        context['active_channel_slug'] = slug=self.kwargs['channel']
        context['filtered_by_user'] = self.kwargs['user']
        context['filtered_by_tag'] = "ninguna"
        return context

class RecordsFilteredViewByTag(RecordsListView):
    def get_queryset(self):
        queryset = super(RecordsListView, self).get_queryset().order_by('created_at').filter(channel__slug=self.kwargs['channel']).filter(tags__slug=self.kwargs['tag'])
        return self.orderQueryByDate(queryset)

    def get_context_data(self, **kwargs):
        context = super(RecordsListView, self).get_context_data(**kwargs)
        # Pass channel data to context
        context['active_channel_name'] = Channel.objects.get(slug=self.kwargs['channel']).name
        context['channel_users'] = self.getChannelUsers
        context['channel_tags'] = self.getChannelTags
        context['active_channel_slug'] = slug=self.kwargs['channel']
        context['filtered_by_tag'] = self.kwargs['tag']
        context['filtered_by_user'] = "ninguno"
        return context
