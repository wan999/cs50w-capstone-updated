from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from PIL import Image

import json

from .models import User, Article, Category, ImageForm, Avatar, Comment, Favorite, Editor

# Create your views here.
def index(request):
    most_recent = None
    most_recent_title = None

    try:
        categories = Category.objects.all()

    except Category.DoesNotExist:
        raise Http404("Categories not found.")    
        
    try:
        # articles = Article.objects.all()

        # .last() most recent
        most_recent = Article.objects.all().order_by('timestamp').last()

        if most_recent != None:
            most_recent_title = most_recent.article_title

    except Article.DoesNotExist:
        raise Http404("Most recent article not found.")
    
    try:
        other_articles = Article.objects.exclude(article_title=most_recent_title)

    except Article.DoesNotExist:
        raise Http404("Articles not found.")
    
    print(categories)
    print(most_recent)
    print(other_articles)
    
    if request.user.is_authenticated:
        try:
            editors = Editor.objects.all()

        except Editor.DoesNotExist:
            raise Http404("Editors not found.")
        
        print(editors)

        check_editor = False
        
        for editor in editors:
            if request.user == editor.member:
                check_editor = True

        return render(request, "index.html", {
            "categories": categories,
            "most_recent" : most_recent, 
            "other_articles": other_articles,
            "check_editor": check_editor
        })
    
    else:

        return render(request, "index.html", {
            "categories": categories,
            "most_recent" : most_recent, 
            "other_articles": other_articles,
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Link to default avatar
            avatar = Avatar.objects.create()
            user.avatar_image = avatar
            print(f"user.avatar_image:{user.avatar_image}")
            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:    
        return render(request, "register.html")
 
def profile(request, username):
    if request.method == "GET":
        try:
            user_profile = User.objects.get(username=username)

        except User.DoesNotExist:
            raise Http404("User not found.")
        
        articles = Article.objects.filter(author=user_profile.id).order_by('-timestamp')

        favorites = Favorite.objects.filter(user_that_favorited=user_profile.id).order_by('-time_favorited')

        print(favorites)

        print(user_profile)
        
        try:
            editors = Editor.objects.all()

        except Editor.DoesNotExist:
            raise Http404("Editors not found.")

        check_editor = False
        
        for editor in editors:
            if user_profile == editor.member:
                check_editor = True

        return render(request, "profile.html", {
            "user_profile": user_profile,
            "articles": articles,
            "favorites": favorites,
            "check_editor": check_editor
        })
    
@login_required
def edit_profile(request, username):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        bio = request.POST["bio"]
        file_data = None

        # Attempt to create new user
        try:
            user_profile = User.objects.get(username=username)

            if first_name:
                user_profile.first_name = first_name
            else:
                return render(request, "edit_profile.html", {
                    "message": "First Name Required."
                })
            
            if last_name:
                user_profile.last_name = last_name
            else:
                return render(request, "edit_profile.html", {
                    "message": "Last Name Required."
                })
            
            if bio:
                user_profile.bio = bio
            else:
                return render(request, "edit_profile.html", {
                    "message": "Biography Required."
                })
            
            if request.FILES:
                file_data = request.FILES['img']
                print(print(f"file_data:{file_data}"))

                try:
                    # check image is valid
                    form = ImageForm(request.POST, request.FILES)

                    print(form.errors)

                    if form.is_valid():
                        cleaned_img = form.cleaned_data['img']
                        avatar = Avatar.objects.create(image=cleaned_img)
                        print(f"avatar:{avatar}")

                        user_profile.avatar_image = avatar
                        print(f"user_profile.avatar_image:{user_profile.avatar_image}")
                        user_profile.save()

                except Avatar.DoesNotExist:
                    raise Http404("Image corrupted.")

        except User.DoesNotExist:
            raise Http404("User not found.")

        user_profile.save()
        
        return HttpResponseRedirect(reverse("profile", args=[username]))

    else:
        try:
            user_profile = User.objects.get(username=username)

        except User.DoesNotExist:
            raise Http404("User not found.")
        
        return render(request, "edit_profile.html", {
            "user_profile": user_profile
        })
        

@login_required     
def create_article(request):
    if request.method == "GET":

        try:
            categories = Category.objects.all()

        except Category.DoesNotExist:
            raise Http404("Categories not found.")
        
        print(categories)

        return render(request, "create_article.html", {
            "categories": categories,
        })
    
    else:

        user = request.user

        try:
            staff = Editor.objects.get(member=user)

        except User.DoesNotExist:
            raise Http404("Not a member of staff")

        try:
            categories = Category.objects.all()

        except Category.DoesNotExist:
            raise Http404("Categories not found.")

        try:
            author = User.objects.get(username=user.username)

        except User.DoesNotExist:
            raise Http404("User not found.")
        
        article_title = request.POST["title"]
        article_content = request.POST["article"]
        image_URL = request.POST["image"]
        category_code = request.POST["category"]

        try:
            category = Category.objects.get(category_code=category_code)

        except Category.DoesNotExist:
            raise Http404("Category not found.")
        
        if Article.objects.filter(article_title=article_title).exists():

            return render(request, "create_article.html", {
                "categories": categories,
                "message": "Article has been published with same title already!"
            })
        
        elif staff:
            try:
                article = Article.objects.create(article_title=article_title, article_content=article_content, category=category, author=author, banner_image=image_URL)
                article.save()

            except IntegrityError:
                return render(request, "create_article.html", {
                    "categories": categories,
                    "message": "Article not published."
                })
            
            print(article)
            
            return HttpResponseRedirect(reverse("single_post", args=[article_title]))
        
        else:
            
            return render(request, "create_article.html", {
                "categories": categories,
                "message": "Not a member of staff"
            })
        
def single_post(request, article_title):

    print(article_title)

    try:
        article = Article.objects.get(article_title=article_title)

    except Article.DoesNotExist:
        raise Http404("Article not found.")
    
    print(article)

    try:
        other_articles = Article.objects.all().exclude(article_title=article_title)

    except Article.DoesNotExist:
        raise Http404("Other articles not found.")
    
    comments = Comment.objects.filter(article_commented_on=article).order_by('-timestamp')

    if comments:
        return render(request, "single-post.html", {
            "article": article,
            "other_articles" : other_articles,
            "comments": comments
        })
    else:
        return render(request, "single-post.html", {
            "article": article,
            "other_articles" : other_articles
        })



@login_required
def delete_article(request, article_title):
    if request.method == "POST":

        current_user = request.user

        print(current_user)

        try:
            article = Article.objects.get(article_title=article_title)

        except Article.DoesNotExist:
            raise Http404("Article not found.")
        
        username = article.author.username
        print(username)

        if (username == current_user.username):
        
            article.delete()
        
            return HttpResponseRedirect(reverse("profile", args=[username]))
        
        else:
            return render(request, "profile.html", {
                "message": "You cannot delete someone else's article!"
            })
        
def search(request):
    if request.method == "GET":

        search_query = request.GET["search_query"]

        try:
            # icontains == case-insensitive 
            article = Article.objects.get(article_title__icontains=search_query)


        except Article.DoesNotExist:

            return render(request, "search_results.html", {
                "search_query": search_query,
                "message" : "No Article Found." 
            })
        
        return render(request, "search_results.html", {
            "article" : article,
            "search_query": search_query,
            "article" : article
        })
        
def filter_articles(request, category):
    print(category)
    single_category = Category.objects.get(category_code=category)
    articles = Article.objects.filter(category=single_category)

    return render(request, "category.html", {
        "articles" : articles,
        "category": single_category

    })

def add_comment(request, article_id):
    print("article_id:"f"{article_id}")

    if request.method == "POST":

        if request.body:
        
            data = json.loads(request.body)
            print("data:"f"{data}")

            comment_user =  data['user']
            comment_content =  data['content']
            article_id = data['article_id']

            try:
                article = Article.objects.get(id=article_id)

            except IntegrityError:
                return render(request, "single-post.html", {
                    "message": "Cannot find article"
                })
            
            article_title = article.article_title
            print("article_title:"f"{article_title}")
            
            comment_instance = Comment.objects.create(user=comment_user, content=comment_content, article_commented_on=article)
            print(comment_instance)
            
            print(HttpResponseRedirect(reverse("single_post", args=[article_title])))

            return HttpResponseRedirect(reverse("single_post", args=[article_title]))
        
@login_required
def add_to_favorites(request, article_id):

    if request.user.is_authenticated:

        user = request.user

        try:
            user_profile = User.objects.get(username=user.username)

        except User.DoesNotExist:
            raise Http404("User not found.")
        
        try:
            article = Article.objects.get(id=article_id)

        except Article.DoesNotExist:
            raise Http404("Article not found.")
        
        if Favorite.objects.filter(article_favorited=article, user_that_favorited=user_profile).exists():

            try:
                other_articles = Article.objects.all().exclude(article_title=article.article_title)

            except Article.DoesNotExist:
                raise Http404("Other articles not found.")
            
            comments = Comment.objects.filter(article_commented_on=article).order_by('-timestamp')

            if comments:
                return render(request, "single-post.html", {
                    "message": "Already Favorited!",
                    "article": article,
                    "other_articles" : other_articles,
                    "comments": comments
                })
            else:
                return render(request, "single-post.html", {
                    "message": "Already Favorited!",
                    "article": article,
                    "other_articles" : other_articles
                })
        
        else:
        
            favorite_instance = Favorite.objects.create(article_favorited=article, user_that_favorited=user_profile)
            
            print(favorite_instance)

            return HttpResponseRedirect(reverse("profile", args=[user.username]))
    
    else:
        return render(request, "login.html", {
            "message": "Login to favorite article!"
        })

    
@login_required    
def delete_favorite(request, article_title):

    if request.user.is_authenticated:

        user = request.user

        if request.method == "POST":

            try:
                article = Article.objects.get(article_title=article_title)
            
            except Article.DoesNotExist:    
                raise Http404("Article not found.")

            try:
                favorite = Favorite.objects.get(article_favorited=article, user_that_favorited=user)

            except Favorite.DoesNotExist:
                raise Http404("Favorite not found.")
            
            username = favorite.user_that_favorited.username
            print(username)

            if (username == user.username):
            
                favorite.delete()
            
                return HttpResponseRedirect(reverse("profile", args=[username]))
            
            else:
                return render(request, "profile.html", {
                    "message": "You cannot delete someone else's favorited article!"
                })
            
    else:
        return render(request, "login.html", {
            "message": "Login to favorite article"
        })

    
