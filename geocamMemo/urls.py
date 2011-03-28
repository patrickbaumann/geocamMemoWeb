# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.conf.urls.defaults import *



urlpatterns = patterns('geocamMemo.views',
    url(r'messages/create', 'create_message'),
    url(r'messages/edit/(?P<message_id>\d+)', 'edit_message'),
    url(r'messages/delete/(?P<message_id>\d+)', 'delete_message'),
    url(r'messages/details/(?P<message_id>\d+)$', 'details'),
    url(r'messages/details/(?P<message_id>\d+).json', 'details_json'),
    url(r'messages/(?P<author_username>[a-zA-Z][a-zA-Z0-9@+.\-]*[a-zA-Z0-9])',
         'message_list'),
    url(r'messages.json','message_list_json'),
    url(r'messages',  'message_list', name="all_message_list"),
    url(r'map', 'memo_map'),
)
