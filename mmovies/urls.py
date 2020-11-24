from django.urls import path,include
from . import views


urlpatterns=[
    path("",views.home,name="home"),
    path("display/<str:section>/",views.display,name="display"),
    path("watchlist/",views.watchlist,name="watchlist"),
    path("<str:name>/read-more/",views.read_more,name="read-more"),
    path("add/",views.add_watchlist,name="add"),
    path("<str:name>/add2/",views.add_watchlist2,name="add2"),
    path("login-/",views.loginpage,name="login"),
    path("register-/",views.register,name="register"),
    path("logout/",views.logoutuser,name="logout"),
    path("remove/",views.remove_watchlist,name="remove"),
    path("watched/",views.check_watch),
    path("choice_/",views.choice_),
]