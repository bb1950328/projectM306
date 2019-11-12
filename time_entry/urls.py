"""time_entry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from time_entry.view import index, login, employee_view, admin


def gen(url, func):
    return [path(url, func),
            path(url + "/", func),
            path(url + ".html", func)]


urlpatterns = [
    path("", index.index),
    *gen("index", index.index),
    *gen("login", login.login),
    *gen("logout", login.logout),
    *gen("employee", employee_view.view),
    *gen("new_absence", employee_view.new_absence),
    *gen("no_permission", index.no_permission),
    *gen("admin", admin.admin),
    *gen("git_pull", admin.git_pull),
]
