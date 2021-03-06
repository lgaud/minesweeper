from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.game, name='game'),
    url(r'^game/create/$', 
        views.create_game, name='create'),
    url(r'^game/(?P<game_id>[0-9]+)/reveal/$', views.reveal, name='reveal'),
    url(r'^game/(?P<game_id>[0-9]+)/mark/$', views.toggle_marking, name='toggle'),
    url(r'^game/stats/$', views.stats, name='stats')
]