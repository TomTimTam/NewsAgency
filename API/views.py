from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import CsrfViewMiddleware
from .models import NewsStory, Category, Region, Author

import time
import datetime
import json

TEXT_CONTENT = "text\plain"
JSON_CONTENT = "application\json"

@csrf_exempt
def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = 'user name = ' + username + ', password = ' + password

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Get author's name for login notification
                author = Author.objects.get(auth_user=user)
                if user.is_authenticated:
                    return HttpResponse(author.name + ' is logged in, Welcome!', status=201, content_type=TEXT_CONTENT)
                    #reponse.set_cookie('session-token', '123456')
                return HttpResponse(data)

            else:
                return HttpResponse('disabled account', status=400, content_type=TEXT_CONTENT)

        else:
            return HttpResponse('invalid login ' + data, status=400, content_type=TEXT_CONTENT)

    else:
        return HttpResponse('request is invalid ' + request.method, status=400, content_type=TEXT_CONTENT)


def handle_logout(request):
    if request.method == 'POST':
        try:
            logout(request)
            return HttpResponse("Logged out successfully, Goodbye!", status=200, content_type=TEXT_CONTENT)
        except:
            return HttpResponse("Logout unsuccessful")


def post_story(request):
    if request.method == 'POST' and request.user.is_authenticated:
        json_data = json.loads(request.body)
        headline = json_data['headline']
        details = json_data['details']
        category_description = json_data['category']
        region_description = json_data['region']

        # Validate user input.
        if len(headline) > 64 or len(details) > 512:
            return HttpResponse('Headline(64) or details(512) were too long', status=503, content_type=TEXT_CONTENT)

        try:
            category = Category.objects.get(description=category_description)
        except:
            return HttpResponse('Invalid category', status=503, content_type=TEXT_CONTENT)

        try:
            region = Region.objects.get(description=region_description)
        except:
            return HttpResponse('Invalid region', status=503, content_type=TEXT_CONTENT)

        try:
            author = Author.objects.get(auth_user=request.user)
        except Author.DoesNotExist or Author:
            return HttpResponse('Invalid author', status=503, content_type=TEXT_CONTENT)

        NewsStory.objects.create(headline=headline,
                                 category=category,
                                 region=region,
                                 author=author,
                                 details=details)
        return HttpResponse(status=201)
    else:
        return HttpResponse('Request is invalid. ' + request.method, status=503)


@csrf_exempt
def get_stories(request):
    if request.method == 'GET':
        if 'story_cat' and 'story_region' and 'story_date' in request.GET:
            category_description = request.GET['story_cat']
            region_description = request.GET['story_region']
            story_date = request.GET['story_date']
        else:
            return HttpResponse('Parameters missing or incomplete', status=404, content_type=TEXT_CONTENT)

        try:
            if category_description == '*':
                categories = Category.objects.all().values_list('id', flat=True)
            else:
                categories = Category.objects.filter(description=category_description).values_list('id', flat=True)
        except:
            return HttpResponse('Category not found', status=404, content_type=TEXT_CONTENT)

        try:
            if region_description == '*':
                regions = Region.objects.all().values_list('id', flat=True).values_list('id', flat=True)
            else:
                regions = Region.objects.filter(description=region_description).values_list('id', flat=True)
        except:
            return HttpResponse('Region not found', status=404, content_type=TEXT_CONTENT)

        # Instantiate datetime as epoch
        if story_date == '*':
            filter_date = datetime.datetime.min
        else:
            try:
                filter_date = datetime.datetime.strptime(story_date, '%d/%m/%Y')
            except:
                return HttpResponse('Invalid datetime', status=404, content_type=TEXT_CONTENT)

        stories = NewsStory.objects.filter(category__id__in=categories, region__id__in=regions, story_datetime__gte=filter_date)

        story_array = []

        for story in stories:
            story_array.append({'key': story.id.__str__(),
                                'headline': story.headline,
                                'story_cat': story.category.description,
                                'story_region': story.region.description,
                                'author': story.author.name,
                                'story_date': story.story_datetime.date().strftime('%d/%m/%Y'),
                                'story_details': story.details})

        stories_dict = {'stories': story_array}

        if stories.count() > 0:
            return JsonResponse(stories_dict, status=200)
        else:
            return HttpResponse(404, 'No data found.', content_type=TEXT_CONTENT)
    else:
        return HttpResponse(404, 'Request is invalid. ' + request.method, content_type=TEXT_CONTENT)


def delete_story(request):
    if request.method == 'POST' and request.user.is_authenticated:
        json_data = json.loads(request.body)
        id_to_delete = json_data['story_key']

        try:
            NewsStory.objects.get(id=id_to_delete).delete()
        except NewsStory.DoesNotExist:
            return HttpResponse("That id doesn't exist", status=503, content_type=TEXT_CONTENT)

        return HttpResponse("Successfully deleted story " + id_to_delete, status=201, content_type=TEXT_CONTENT)
    else:
        return HttpResponse("Failed to delete that story", status=503, content_type=TEXT_CONTENT)
