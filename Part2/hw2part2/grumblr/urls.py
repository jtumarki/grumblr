#urls
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'grumblr.views.home'),
    url(r'^grumblr$', 'grumblr.views.home'),
    url(r'^add-grumbl', 'grumblr.views.add_grumbl'),
    url(r'^following$', 'grumblr.views.following'),
    url(r'^profile$', 'grumblr.views.show_profile'),
    url(r'^editprofile$', 'grumblr.views.show_edit_profile'),
    url(r'^submit-edit', 'grumblr.views.edit_profile'),
    url(r'^search', 'grumblr.views.search'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/grumblrlogin.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'grumblr.views.register'),
)