from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


# index view (just redirect to login page)
def index(request):
    return HttpResponseRedirect('/login')


# this view will run after successfull login
@login_required
def logged_in(request):
    return render_to_response(
        'logged_in.html',
        context_instance=RequestContext(request)
    )
