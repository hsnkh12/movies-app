from django.contrib import admin
from .models import sections,all,user_watchlist_child,user_watchlist_parent,actors


admin.site.register(sections)
admin.site.register(all)
admin.site.register(actors)
admin.site.register(user_watchlist_parent)
admin.site.register(user_watchlist_child)