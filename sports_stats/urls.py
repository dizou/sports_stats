from django.conf.urls import patterns, include, url
from django.contrib import admin
from sports_stats.views.views import IndexView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
