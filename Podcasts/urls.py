from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.signup, name='signup'),
    url(r'^select_genre', views.select_genre, name='select_genre'),
    url(r'^results', views.search_results, name='results'),
    url(r'^confirmation', views.confirmation, name='confirmation'),
    url(r'^complete_activity', views.complete_activity, name='complete_activity')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
