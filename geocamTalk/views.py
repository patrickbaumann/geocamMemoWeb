# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from geocamTalk.models import TalkMessage
from geocamTalk.forms import GeocamTalkForm
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Q, Count
import json
    
@login_required
def message_list(request, recipient_username=None, author_username=None):    
    if recipient_username is not None:
        recipient = get_object_or_404(User, username=recipient_username)
    else:
        recipient = None
        
    if author_username is not None:
        author = get_object_or_404(User, username=author_username)
    else:
        author = None                                                                                         
    return render_to_response('geocamTalk/message_list.html', 
                              dict(gc_msg=TalkMessage.getMessages(recipient,author), 
                                   recipient=recipient, 
                                   author=author), 
                               context_instance=RequestContext(request))

@login_required
def feed_messages(request, recipient_username=None, author_username=None):
    if recipient_username is not None:
        recipient = get_object_or_404(User, username=recipient_username)
    else:
        recipient = None
        
    if author_username is not None:
        author = get_object_or_404(User, username=author_username)
    else:
        author = None
        
    messages = TalkMessage.getMessages(recipient, author)
    return HttpResponse(json.dumps([msg.getJson() for msg in messages]))
    
@login_required
def index(request):
    return render_to_response('geocamTalk/home.html',
                              dict(), 
                              context_instance=RequestContext(request))

@login_required
def create_message(request):
    if request.method == 'POST':
        form = GeocamTalkForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            # Since revisions are now saved to db, this timestamp
            # can't just be auto set since we want to preserve from creation time
            msg.content_timestamp = datetime.now()
            msg.save()
            form.save_m2m()
            return HttpResponseRedirect('/talk/messages')
        else:
            return render_to_response('geocamTalk/message_form.html',
                                  dict(form=form),
                                  context_instance=RequestContext(request))
    else:
        form = GeocamTalkForm()
        return render_to_response('geocamTalk/message_form.html',
                                  dict(form=form),                               
                                  context_instance=RequestContext(request))