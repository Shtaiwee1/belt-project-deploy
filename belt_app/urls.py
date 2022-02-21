from django.urls import path
from . import views
urlpatterns = [
    path('', views.index ),
    path('process_reg', views.process_reg ),
    path('process_login', views.process_login ),
    path('wishes', views.wishes),
    path('wishes/edit/<int:wish_id>', views.edit_wishes),
    path('process_edit_wish/<int:wish_id>', views.process_edit_wishes),
    path('wishes/new', views.create_wish),
    path('process_new_wish', views.process_new_wish),
    path('remove_wish/<int:wish_id>', views.remove_wish),
    path('wishes/stats', views.wishes_stats),
    path('clear', views.clear ),]