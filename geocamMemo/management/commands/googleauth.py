# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.core.management.base import BaseCommand, CommandError
from example import settings
import httplib
import urllib
import re
import os

class Command(BaseCommand):
    args = 'none'
    help = 'generate the authentication module needed to push c2dm messages to the google servers'

    def handle(self, *args, **options):
        
        email = raw_input("Please enter your gmail address: ")
        password = raw_input("Please enter your gmail password: ")

        params = urllib.urlencode({
                 'Email': email,
                 'Passwd': password,
                 'accountType': 'GOOGLE',
                 'source':'gov.nasa.arc.geocam.talk',
                 'service':'ac2dm',
                 })
        
        # need the following headers set per http://code.google.com/android/c2dm/index.html#push
        headers = { "Content-Type":"application/x-www-form-urlencoded",
                    "Content-Length":len(params)
                    }
        
        # NOW SEND THE REQUEST TO GOOGLE SERVERS
        # first we need an https connection that ignores the certificate (for now)
        httpsconnection = httplib.HTTPSConnection("www.google.com", 443)
        httpsconnection.request("POST", "/accounts/ClientLogin", params, headers)
        response = httpsconnection.getresponse()
        response_body = response.read()
        authstring = re.search('(?<=Auth=)[-_a-zA-Z0-9]+$',response_body).group(0)
        
        authfile = open(settings.APP + os.sep + "geocamMemo" + os.sep + "authentication.py", "w+")
        
        authfile.write('GOOGLE_TOKEN = "' + authstring + '"')