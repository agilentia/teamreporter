"""teamreporterapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from teamreporter.views import IndexView, UserView, TeamView, RoleView, ReportView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^team/$', TeamView.as_view(), name="team_view"),
    url(r'^team/(?P<team_id>\d+)/report/questions/?$', ReportView.as_view(), name="report_view"), #treating this as a questions endpoint for now
    url(r'^team/(?P<team_id>\d+)/report/questions/(?P<question_id>\d+)/?$', ReportView.as_view(), name="questions_view"), #a bit hacky, but can make separate resource later for questions
    url(r'^team/(?P<team_id>\d+)/users/?$', UserView.as_view(), name="user_view"),
    url(r'^team/(?P<team_id>\d+)/users/(?P<user_id>\d+)/?$', UserView.as_view(), name="user_detail_view"), #a bit hacky, but can make separate resource later for questions
    url(r'^role/$', RoleView.as_view(), name="role_view"),
    url('^$', IndexView.as_view(), name='index'),
]
