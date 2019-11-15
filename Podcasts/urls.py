from django.conf.urls import url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^results', views.search_results, name='results'),
    url(r'^confirmation', views.confirmation, name='confirmation')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
