from django.shortcuts import render_to_response, redirect, get_object_or_404, get_list_or_404, render
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
    c = {"entry_list": entry_list,
                        "commentform": commentform,
                        "category_list": Category.objects.all(),
                        "setting": setting,
        }
    return render(request, "cblog/cblog_index.html", c)

def cblog_entry(request, slug, id):
    try:
        entry=Entry.objects.get(id=id)
        comments=Comment.objects.filter(entry=entry)
    except:
        raise Http404()

    commentform=CommentForm()
    c = {
            "entry": entry,
            "commentform":commentform,
            "comment_list":comments,
            "category_list": Category.objects.all(),
            "setting": setting,
        }
    return render(request, "cblog/cblog_entry.html", c)


@login_required(login_url="/blog/login")
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

    c = {"form":form,
        "setting": setting,
        "id": id,
        }
    return render(request,"cblog/cblog_edit.html",c)

@login_required(login_url="/blog/login")
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

@login_required(login_url="/blog/login")
def cblog_delete_comment(request, comment_id, entry_id):
    entry=get_object_or_404(Entry, id=entry_id)
    comment=get_object_or_404(Comment,id=comment_id)
    comment.delete()
    return redirect("%s"%reverse(cblog_entry, args=(entry.slug, entry.id)))

def cblog_category(request, category_id=None):
    if category_id:
        category_list=get_list_or_404(Category, id=category_id)
    else:
        category_list=Category.objects.all()

    category_info_list=[]
    for c in category_list:
        if  request.user.is_authenticated():
            cate_info={'category':c, 'entries':Entry.objects.filter(categories=c)}
        else:
            cate_info={'category':c, 'entries':Entry.objects.filter(categories=c, isdraft=False)}
        category_info_list.append(cate_info)

    reqcontext={
                    "category_list":category_info_list,
                    "setting":setting
                }
    return render(request, "cblog/cblog_category.html",reqcontext)

@login_required(login_url="/blog/login")
def cblog_delete_category(request, category_id):
    category=get_object_or_404(Category,id=category_id)
    entry_list=Entry.objects.filter(categories=category_id)
    for e in entry_list:
        if len(e.categories.all()) <= 1:
            e.categories.add(Category.objects.get_or_create(title='Uncategorized')[0])
            e.save()
    category.delete()

    return redirect("%s"%reverse(cblog_category))

def cblog_datelist_article(request, year=None):
    if year:
        if request.user.is_authenticated():
            datelist=[{'year': year, 'entries':get_list_or_404(Entry, pub_date__year=year)}]
        else:
            datelist=[{'year': year, 'entries':get_list_or_404(Entry, pub_date__year=year,isdraft=False)}]

    else:
        datelist=[]
        if request.user.is_authenticated():
            dates=Entry.objects.all().datetimes('pub_date','year', order='DESC')
        else:
            dates=Entry.objects.filter(isdraft=False).datetimes('pub_date','year', order='DESC')

        for d in dates:
            entrylist=Entry.objects.filter(pub_date__year=d.year)
            datedict={}
            if entrylist:
                datedict['year']=d.year
                datedict['entries']=entrylist
                datelist.append(datedict)

    reqcontext={
        "article_year_list": datelist,
        "setting":setting
    }
    return render(request, "cblog/cblog_articlelist.html",reqcontext)


@login_required(login_url="/blog/login")
def cblog_post_upload(request, slug):
    try:
        e=Entry.objects.get(slug=slug)
        id=e.id
    except Entry.DoesNotExist:
        id=""

    return cblog_edit(request,id)


@login_required(login_url="/blog/login")
def cblog_file_upload(request):
    from django import forms
    from django.template import Template

    class ImagesUploadForm(forms.Form):
        images=forms.FileField()

    def upload_images(f):
        with open('/tmp/test.jpg', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    if request.method == 'POST':
        form=ImagesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f=request.FILES['images']
            upload_images(f)
            return redirect("%s"%request.get_full_path())
    else:
        form=ImagesUploadForm()

    templatestr="""
    <form action="{% url 'reverse_cblog_file_upload' %}" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="save" >
    </form>
    """

    template=Template(templatestr)
    html=template.render(context=RequestContext(request,{'form':form}))
    return HttpResponse(html)


