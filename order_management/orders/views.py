from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Orders
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from taggit.models import Tag


def home(request):
    orders = get_object_or_404(Orders, id=request.POST.get('id'))
    is_favourite = False
    if orders.favourite.filter(id):
        is_favourite =True

    context ={
        'orders': Orders.objects.all()
    }
    return render(request, 'orders/home.html', context)

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin,self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class OrdersListView(ListView):
    model = Orders
    template_name = 'orders/home.html'
    context_object_name = 'orders'
    ordering = ['-date_posted']

class OrdersDetailView(DetailView):
    model = Orders


class OrdersCreateView(LoginRequiredMixin, CreateView):
    model = Orders
    fields = ['title', 'content','tags']

    def form_valid(self, form):
        form.instance.orderer = self.request.user
        return super().form_valid(form)

class OrdersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Orders
    fields = ['title', 'content','tags']

    def form_valid(self, form):
        form.instance.orderer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.orderer:
            return True
        return False

def favourite_list(request):
   # user = request.user
    new = Orders.objects.filter(favourites=request.user)
    return render(request,'orders/favourite_list.html',{'new':new})

def search_tag(request):
    if request.method=='POST':
        searched = request.POST['searched']
        searched_tags = Orders.objects.filter(tags__name__icontains=searched)
        return render(request,'orders/tag_search.html',{'searched':searched,'searched_tags':searched_tags})

@login_required
def favourite_add(request, id):
    orders = get_object_or_404(Orders, id=id)
    if orders.favourites.filter(id=request.user.id).exists():
        orders.favourites.remove(request.user)
    else:
        orders.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

class OrdersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Orders
    success_url = '/'

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.orderer:
            return True
        return False

class TagIndex(ListView,TagMixin):
    model = Orders
    template_name = 'orders/order_tag.html'
    context_object_name = 'orders'
    tag = Orders.objects.filter(tags__name__icontains=Tag)

    def get_queryset(self):
        return Orders.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


def about(request):
    return render(request, 'orders/home.html')
