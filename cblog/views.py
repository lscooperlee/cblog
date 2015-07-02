from django.shortcuts import render_to_response, HttpResponseRedirect, redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.template import RequestContext
from cblog.models import Entry, Category
from cblog.config import setting
from cblog.forms import EntryForm

def cblog_login(request):
    if request.user.is_authenticated():
            return redirect('%s' %reverse(cblog_index))

    para = {'template_name': 'cblog/cblog_login.html', 'extra_context': {"setting": setting}}
    return auth_views.login(request, **para)

def cblog_logout(request):
    return auth_views.logout(request,next_page="%s"%reverse(cblog_index))

def cblog_index(request):
    c = RequestContext(request,
                       {"entry_list": Entry.objects.all(),
                        "category_list": Category.objects.all(),
                        "setting": setting,
                        "user": User}
                       )
    return render_to_response("cblog/cblog_index.html", c)


@login_required(login_url="/cblog/login")
def cblog_edit(request):
    if request.method=='POST':
        form=EntryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form)
    else:
        form=EntryForm()

#    c={"user": User,"setting":setting,"form":form}
    c = RequestContext(request,
                       {"form":form,
                        "setting": setting,
                        "user": User}
                       )
    return render_to_response("cblog/cblog_edit.html",c)
