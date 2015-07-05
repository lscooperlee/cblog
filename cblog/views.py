from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from cblog.models import Entry, Category, Comment
from cblog.config import setting
from cblog.forms import EntryForm, CommentForm

def cblog_login(request, context={}):
    if request.user.is_authenticated():
            return redirect('%s' %reverse(cblog_index))
    context['setting']=setting
    if 'next' not in request.GET:
        context['next']=request.get_full_path()
    para = {'template_name': 'cblog/cblog_login.html', 'extra_context': context}
    return auth_views.login(request, **para)

def cblog_logout(request):
    return auth_views.logout(request,next_page="%s"%reverse(cblog_index))

def cblog_index(request):

    if request.user.is_authenticated():
        all_list=Entry.objects.all()
    else:
        all_list=Entry.objects.filter(isdraft=False)

    paginator=Paginator(all_list,10)
    page=request.GET.get('page')
    try:
        entry_list=paginator.page(page)
    except PageNotAnInteger:
        entry_list=paginator.page(1)
    except EmptyPage:
        entry_list=paginator.page(paginator.num_pages)

    commentform=CommentForm()
    c = RequestContext(request,
                       {"entry_list": entry_list,
                        "commentform": commentform,
                        "category_list": Category.objects.all(),
                        "setting": setting,
                        "user":User}
                       )
    return render_to_response("cblog/cblog_index.html", c)

def cblog_entry(request, slug, id):
    try:
        entry=Entry.objects.get(id=id)
        comments=Comment.objects.filter(entry=entry)
    except:
        raise Http404()

    commentform=CommentForm()
    c = RequestContext(request,
                       {"entry": entry,
                        "commentform":commentform,
                        "comment_list":comments,
                        "category_list": Category.objects.all(),
                        "setting": setting,
                        "user":User}
                       )
    return render_to_response("cblog/cblog_entry.html", c)


@login_required(login_url="/cblog/login")
def cblog_edit(request, id=""):

    if id:
        entry=get_object_or_404(Entry, pk=id)
    else:
        entry=None

    if request.method=='POST':
        form=EntryForm(request.POST,instance=entry)
        if form.is_valid():
            form.save()
            return redirect("%s"%reverse(cblog_entry, args=(form.instance.slug,form.instance.id)))
    else:
        form=EntryForm(instance=entry)

    c = RequestContext(request,
                       {"form":form,
                        "setting": setting,
                        "id": id,
                        "user": User}
                       )
    return render_to_response("cblog/cblog_edit.html",c)

@login_required(login_url="/cblog/login")
def cblog_delete(request, id):

    try:
        entry=Entry.objects.get(pk=id)
        if entry.isdraft:
            comments=Comment.objects.filter(entry=entry)
            comments.delete()
            entry.delete()
        else:
            entry.isdraft=True
            entry.save(update_fields=['isdraft'])

    except Entry.DoesNotExist:
        raise Http404()

    return redirect('%s' %reverse(cblog_index))


def cblog_edit_comment(request, entry_id, comment_id=None):

    if request.method == 'POST':
        try:
            entry=Entry.objects.get(id=entry_id)
            commentform=CommentForm(request.POST)
            if commentform.is_valid():
                commentform.instance.entry=entry
                commentform.save()

        except Entry.DoesNotExist:
            raise Http404()

    if request.GET.get('index','NO') == 'NO':
        return redirect("%s"%reverse(cblog_entry, args=(entry.slug,entry.id)))
    else:
        return redirect("%s"%reverse(cblog_index))

def cblog_delete_comment(request, comment_id, entry_id):
    entry=get_object_or_404(Entry, id=entry_id)
    comment=get_object_or_404(Comment,id=comment_id)
    comment.delete()
    return redirect("%s"%reverse(cblog_entry, args=(entry.slug, entry.id)))
