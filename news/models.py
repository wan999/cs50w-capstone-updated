from django.db import models
from PIL import Image
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AbstractUser

class ImageForm(forms.Form):
    img = forms.ImageField()

class Avatar(models.Model):
    image = models.ImageField(default='./static/avatar_default.jpg')

def __str__(self):
    return f"Avatar: {self.image}"

class User(AbstractUser):
    pass
    first_name = models.TextField(blank=False, default="John")
    last_name = models.TextField(blank=False, default="Doe")
    bio = models.TextField(blank=True)
    avatar_image = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True, related_name="avatar")

    def __str__(self):
        return f"Username: {self.username}, First Name: {self.first_name}, Last Name: {self.last_name} Bio is {self.bio}, avatar_image: {self.avatar_image}"
    
class Category(models.Model):
    # category = models.CharField(max_length=255, default="World", unique=True)
    WORLD = "WRL"
    USA = "USA"
    TECH = "TEC"
    DESIGN = "DSG"
    CULTURE = "CUL"
    BUSINESS = "BUS"
    POLITICS = "POL"
    OPINION = "OPI"
    SCIENCE = "SCI"
    HEALTH = "HTL"
    STYLE = "STY"
    TRAVEL = "TRA"

    CATEGORIES = {
        WORLD: "World",
        USA: "USA",
        TECH: "Technology",
        DESIGN: "Design",
        CULTURE: "Culture",
        BUSINESS: "Business",
        POLITICS: "Politics",
        OPINION: "Opinion",
        SCIENCE: "Science",
        HEALTH: "Health",
        STYLE: "Style",
        TRAVEL: "Travel",
    }
    category_code = models.CharField(
        max_length=10,
        choices=CATEGORIES,
        default=WORLD,
    )

    def __str__(self):
        return self.CATEGORIES[self.category_code]
    
class Article(models.Model):
    article_title = models.TextField(blank=False)
    article_content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    banner_image = models.URLField()

    def __str__(self):
        return f"{self.author} wrote article: {self.article_content} in {self.category} at {self.timestamp} with banner URL: {self.banner_image}"
    
class Comment(models.Model):
    user = models.CharField(max_length=64)
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    article_commented_on = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_commented_on") 

    def __str__(self):
        return f"{self.user} wrote {self.content} at {self.timestamp} about {self.article_commented_on}"
    
class Favorite(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    article_favorited = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favorited_articles")
    user_that_favorited = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_that_favorited")
    time_favorited = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_that_favorited} favorited {self.article_favorited} at {self.time_favorited}"
    
    

