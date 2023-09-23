"""Here we create WEB Pages. views.py must return a HTML response or Exception

Below 'posts' is dummy data used b4 models in model.py was created.
This isn't in use
YOUTUBE video for POST MODEL: https://youtu.be/aHC3uTkT9r8

posts = [
    {
        'author': 'Arthur',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': '5th November, 2021'
    },
    {
        'author': 'Tacitus Kilgore',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': '7th November, 2021'
    }
]

Posts will be displayed in HOME PAGE through context arg

def home(request):
    # HOME PAGE
    context={
        'posts': Post.objects.all() 
    } # the value is from Post class in models.py.
    # Value feeded through cmd interface eg: post_1 = Post(title='Blog 1', content= 'xxx', author= user)
    # user was defined through user = User.objects.filter(username='Arthur').first()
    # for post 2 user_id was used eg: post_2 = Post(title='Blog 2', content= 'xxx', author_id= user_id)
    # for 3rd post: user.post_set.create(title='Blog 3', content= 'xxx')
    # No need for author field for 3rd post as user was already set previously. 
    return render(request, 'blog/home.html', context)
    # 1st arg is always request. 2nd is loc of template in sub dir. 3rd is context.
    # Title can be seen in Tab of browser.
    # Deafult title for Home Page (Django Blog) as mentioned in home.html in templates/blog

def home can be replaced with class PostListView. This class gives us more functionality like setting 
the order of blog posts
"""

# 'RENDER' from 'SHORTCUTS' to render the Templates from Templates dir
# get_object_or_404 look up class UserListView 
from django.shortcuts import render, get_object_or_404
# LoginRequiredMixin make sure user is logged in b4 CREATING POST. If not redirect to Login page.
# UserPassesTestMixin makes sure users can't UPDATE other people's post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User # for class UserListView
# for thier respective child classes
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post # '.' for current dir

def about(request):
    # ABOUT PAGE
    return render(request, 'blog/about.html', {'title': 'About'})
    # Only Title.

class PostListView(ListView):
    model = Post
    # By default ListView  module looks for HTML template in
    # <app>/<model>_<viewtype>.html i.e blog/post_html which doesn't exist
    # in our dir so we change it to blog/home/html
    template_name = 'blog/home.html'
    # By default ListView  module will call 'posts' in line 26 as object list
    # So we need a new variable to be called posts instead
    context_object_name = 'posts'
    ordering = ['-date_posted'] # - for newest to oldest
    paginate_by = 5 # Number of POSTS per page 

"""
In the HOME Page we see Usernames associated with each POST. This class takes us to
all the posts made by that Author if we click their displayed Username (it has url).
Similar to class PostListView. Add url_pattern in blog/urls.py
"""
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']. Add this to return at the end
    paginate_by = 5

    #  Overide the queryset made by code from class PostListView to get the Posts
    # from specific Auhtor
    # get_queryset not get_query_set. This func already exists & we are overiding it
    def get_queryset(self):
        # get user object or give 404 error.
        # get the object from User model. Get username from url.
        # kwargs is the query parameters
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # limiting and priting the list of posts to the specific Author (author=user)
        return Post.objects.filter(author=user).order_by('-date_posted')

"""
in blog/urls.py import from .views import PostListView then in url_patterns replace
views.home with PostListView.as_view()
.as_view is required as Django needs to know we are passing the module as a view func 
"""

"""
This class will allow us to open the posts.
Similarly add url_pattern. href added to line 16 in template/blog/home.html to allow us
to open Posts from Home Web page.
"""
class PostDetailView(DetailView):
    model = Post
    # Default template convention is <app>/<model>_<viewtype>.html. So we cr8
    # a template in templates dir as blog/post_detail.html

"""
Allows us to create/publish Posts. By convention mentioned abv in line 60,
template of this class should be blog/post_create.html but this class will be sharing
template with PostUpdateView so blog/post_form.html templte is created instead of
the previous conveention based one.

blog/templates/blog/base.html nav sections contains button (New Post) for logged user
to Create Post
url_pattern= post/create_post/ in blog/urls.py
"""
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'video'] #Post title.

    # Now we have to attach the logged in user so that we can actually cr8 the post.
    # This is save the post but Django won't know where to take the user after the 
    # post is made so we use reverse func in blog/models.py which will take us to the
    # Post Detail page where we can see our new post. reverse func is used instead of
    # redirect bcoz reverse take us back to page with newly uploaded data. In this redirect
    # func will give error as it can only fetch unloaded pages.

    def form_valid(self, form):
        # author = current logged in user
        form.instance.author = self.request.user
        # this gets run anyway but specifying it makes sure it runs after we have
        # set author = user.
        return super().form_valid(form) # don't forget the form in bracs

"""
Allows us to Update Published Posts. Same as class PostCreateView
url_pattern in blog/urls.py
LoginRequiredMixin & UserPassesTestMixin should be in the left bcoz they have run
first & perform validation b4 functions like UpdateView or DeleteView start.
"""

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'video']

    def form_valid(self, form):
        form.instance.author = self.request.user # user authoring POST
        return super().form_valid(form)
    
    # Currently any logged in user can UPDATE anyone's POST. The func below
    # checks a valid user is updating thier Published Post.
    def test_func(self):
        post = self.get_object() # gets the post user is trying to update
        
        # checks whether the current user is the author

        if self.request.user == post.author:
            return  True
        return False

"""
To DELETE POSTS. New Template created to confirm POST DELETION
in (templates/blog/post_confirm_delete.html). Follows convention mentioned in
line 60.
Add url_pattern after being done here.
"""        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # Takes us to HOME Page on successful deletion

    def test_func(self):
        post = self.get_object() # gets the post user is trying to update
        
        # checks whether the current user is the author

        if self.request.user == post.author:
            return  True
        return False