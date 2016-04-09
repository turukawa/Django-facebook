try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url
from django.conf import settings

# help autodiscovery a bit
from django_facebook import admin, views, example_views

urlpatterns = [
    url(r'^connect/$', views.connect,
        name='facebook_connect'),
    url(r'^disconnect/$', views.disconnect,
        name='facebook_disconnect'),
    url(r'^example/$', views.example,
        name='facebook_example'),
]

dev_patterns = [
    url(r'^lazy_decorator_example/$', example_views.lazy_decorator_example,
        name='facebook_lazy_decorator_example'),
    url(r'^decorator_example/$', example_views.decorator_example,
        name='facebook_decorator_example'),
    url(r'^decorator_example_scope/$', example_views.decorator_example_scope,
        name='facebook_decorator_example_scope'),
    url(r'^wall_post/$', example_views.wall_post,
        name='facebook_wall_post'),
    url(r'^checkins/$', example_views.checkins,
        name='facebook_checkins'),
    url(r'^image_upload/$', example_views.image_upload,
        name='facebook_image_upload'),
    url(r'^canvas/$', example_views.canvas,
        name='facebook_canvas'),
    url(r'^page_tab/$', example_views.page_tab,
        name='facebook_page_tab'),
    url(r'^open_graph_beta/$', example_views.open_graph_beta,
        name='facebook_open_graph_beta'),
    url(r'^remove_og_share/$', example_views.remove_og_share,
        name='facebook_remove_og_share'),
]

# when developing enable the example views
if settings.DEBUG or getattr(settings, 'TESTING', False):
    # only enable example views while developing
    urlpatterns += dev_patterns

# putting this here instead of models.py reduces issues with import ordering
if getattr(settings, 'AUTH_PROFILE_MODULE', None) == 'django_facebook.FacebookProfile':
    '''
    If we are using the django facebook profile model, create the model
    and connect it to the user create signal
    '''

    from django.db.models.signals import post_save
    from django_facebook.models import FacebookProfile
    from django_facebook.utils import get_user_model

    # Make sure we create a FacebookProfile when creating a User
    def create_facebook_profile(sender, instance, created, **kwargs):
        if created:
            FacebookProfile.objects.create(user=instance)

    post_save.connect(create_facebook_profile, sender=get_user_model())
