from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=50)
    auth_user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)


class Category(models.Model):
    id = models.AutoField
    description = models.CharField(max_length=7)


class Region(models.Model):
    id = models.AutoField
    description = models.CharField(max_length=4)


class NewsStory(models.Model):
    id = models.AutoField
    headline = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    story_datetime = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=512)

class NewsStoryDTO(object):


    def __init__(self, story):
        self.id = str.join(story.id.__str__()),
        self.headline = story.headline,
        self.description = story.category.description,
        self.region = story.region.description,
        self.author = story.author.name,
        self.date = story.story_datetime.date().strftime('%d/%m/%Y'),
        self.details = story.details

