from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

#helps with search
from django.db.models import Q

from grumblr.models import *

@login_required
def home(request):
    # Shows home stream page with user's grumbls
    items = Grumbl.objects.filter(user=request.user).order_by('-created')
    return render(request, 'grumblr/homestream.html', {'items' : items})

@login_required
def search(request):
    # Shows search results
    searchtext = ''

    if 'searchtext' in request.POST or request.POST['searchtext']:
        searchtext = request.POST['searchtext']

    items = Grumbl.objects.filter(Q(text__icontains=searchtext)).order_by('-created')
    return render(request, 'grumblr/search.html', {'items' : items})

@login_required
def following(request):
    # Shows page with grumblrs that the user is following (for now, shows all EXCEPT user)
    items = Grumbl.objects.filter(~Q(user=request.user)).order_by('-created')
    return render(request, 'grumblr/following.html', {'items' : items})

@login_required
def show_profile(request):
	#shows current user profile with filled in information. Assume only one object exists for
	#the given user since usernames are unique and every time you edit the info it is replaced
	info = UserInfo.objects.get(user=request.user)
	return render(request, 'grumblr/myprofile.html', {'info' : info})

@login_required
def show_edit_profile(request):
	#Displays the edit profile page. Have current info already displayed
	info = UserInfo.objects.get(user=request.user)
	return render(request, 'grumblr/editprofile.html', {'info' : info})

@login_required
def edit_profile(request):
	#Submits data to actually edit the user's profile page

    errors = []
    info = UserInfo.objects.get(user=request.user)

    context = {'info' : info, 'errors' : errors}

    if not 'password1' in request.POST or not request.POST['password1']:
	    errors.append('Old password is required.')

    else:
        if not request.user.check_password(request.POST['password1']):
	        errors.append('Incorrect old password.')

    if errors:
        return render(request, 'grumblr/editprofile.html', context)

    if 'name' in request.POST or request.POST['name']:
        info.name = request.POST['name']

    if 'blurb' in request.POST or request.POST['blurb']:
        info.blurb = request.POST['blurb']

    if 'about_me' in request.POST or request.POST['about_me']:
        info.about_me = request.POST['about_me']

    if 'school' in request.POST or request.POST['school']:
        info.school = request.POST['school']

    if 'contact' in request.POST or request.POST['contact']:
        info.contact = request.POST['contact']

    if 'password2' in request.POST or request.POST['password2']:
        request.user.set_password(request.POST['password2'])

    request.user.save()
    info.save()

    return render(request, 'grumblr/myprofile.html', context)

@login_required
def add_grumbl(request):
    errors = []

    # Creates a new item if it is present as a parameter in the request
    if not 'grumbltext' in request.POST or not request.POST['grumbltext']:
	errors.append('You must enter text in a grumbl.')
    else:
	new_item = Grumbl(text=request.POST['grumbltext'], user=request.user)
	new_item.save()

    items = Grumbl.objects.filter(user=request.user).order_by('-created')
    context = {'items' : items, 'errors' : errors}
    return render(request, 'grumblr/homestream.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/grumblrregister.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
	errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
	context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
	errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
	errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
	errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
	errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/grumblrregister.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    #also adds blank info to profile data
    user_info = UserInfo(user=new_user, name='', blurb='', about_me='', school='', contact='')
    user_info.save()

    login(request, new_user)
    return redirect('/grumblr')

