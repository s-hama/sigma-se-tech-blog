from django.db.models import Q
from django.views import generic
from .models import Post
import logging
 	
class BaseListView(generic.ListView):
    paginate_by = 10 
    def base_queryset(self):
        queryset = Post.objects.filter(
            is_publick=True).order_by('-created_at')
        logging.getLogger('command').debug('ON View.py > BaseListView')
        return queryset

class PostIndexView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        keyword = self.request.GET.get("quick")
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword))
        logging.getLogger('command').debug('ON View.py > PostIndexView')

        # Log the contents of queryset
        queryset_list = list(queryset.values())  # Convert QuerySet to list of dictionaries
        logging.getLogger('command').debug(f'QuerySet contents: {queryset_list}')

        return queryset

class CategoryView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        category = self.kwargs.get("small")
        if category:
            queryset = queryset.filter(category__name=category)
        else:
            category = self.kwargs.get("big")
            queryset = queryset.filter(category__parent__name=category)
        logging.getLogger('command').debug('ON View.py > CategoryView')
        return queryset

class TagView(BaseListView):
    def get_queryset(self):
        tag = self.kwargs["tag"]
        queryset = self.base_queryset().filter(tag__name=tag)
        logging.getLogger('command').debug('ON View.py > TagView')
        return queryset

class ProfileView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class ContactView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class PpolicyView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class PostDetailView(generic.DetailView):
    model = Post
    def get_object(self, queryset=None):
        post = super().get_object()
        if str(post.category) not in str("PaidContent") and post.is_publick:
            return post
        elif str(post.category) in str("PaidContent") and post.is_publick and self.request.user.is_authenticated:
            return post
        else:
            raise Http404
