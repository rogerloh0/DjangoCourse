from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm

#GET -> 1 object
#filter -> [] objects

# def blog_post_detail_page(req, slug):
#   # try:
#   #   obj = BlogPost.objects.get(id=str(post_id))
#   # except BlogPost.DoesNotExist:
#   #   raise Http404
#   # except ValueError:
#   #   raise Http404
#   # queryset = get_object_or_404(BlogPost, slug=slug)
#   queryset = BlogPost.objects.filter(slug=slug)
#   if queryset.count() == 0:
#     raise Http404
#   obj = queryset.first()
#   template_name = 'blog_post_detail.html'
#   context = {"object": obj}
#   return render(req, template_name, context)

#CRUD
#Create - Retreive - Update - Delete
#GET - Retreive/List
#POST - Create/Update/Delete

def blog_post_list_view(req):
  # list out objects
  # could be search
  qs = BlogPost.objects.all().published()
  if req.user.is_authenticated:
    my_qs = BlogPost.objects.filter(user=req.user)
    qs = (qs | my_qs).distinct()
   # queryset -> list of python object
  # qs = BlogPost.objects.filter(title_icontains='hello')
  template_name = 'blog/list.html'
  context = {'object_list': qs}
  return render(req, template_name, context)

def blog_post_detail_view(req, slug):
  # 1 object -> detail view
  # ? use a form
  obj = get_object_or_404(BlogPost, slug=slug)
  template_name = 'blog/detail.html'
  context = {"object": obj}
  return render(req, template_name, context)

def blog_post_update_view(req, slug):
  obj = get_object_or_404(BlogPost, slug=slug)
  form = BlogPostModelForm(req.POST or None, instance=obj)
  if form.is_valid():
    form.save()
    return redirect(f'{obj.get_absolute_url()}')
  template_name = 'form.html'
  context = {"title": f"Update {obj.title}", 'form':form}
  return render(req, template_name, context)

# @login_required
@staff_member_required
def blog_post_create_view(req):
  # create objects
  # ? use a form
  # req.user -> return something
  form = BlogPostModelForm(req.POST or None, req.FILES or None)
  if form.is_valid():
    # print(form.cleaned_data)
    # title = form.cleaned_data['title']
    # obj = BlogPost.objects.create(title = title)
    # obj = BlogPost.objects.create(**form.cleaned_data)
    obj = form.save(commit=False)
    obj.user = req.user
    obj.save()

    form = BlogPostModelForm()
  template_name = 'form.html'
  context = {'form': form}
  return render(req, template_name, context)
  
@staff_member_required
def blog_post_delete_view(req, slug):
  obj = get_object_or_404(BlogPost, slug=slug)
  template_name = 'blog/delete.html'
  if req.method == "POST":
    obj.delete()
    return redirect('/blog')
  context = {"object": obj}
  return render(req, template_name, context)
