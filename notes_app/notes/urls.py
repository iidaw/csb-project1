from django.urls import path

from .views import index, addNoteView, noteView, deleteNoteView, loginView, logoutView

urlpatterns = [
    path('', index, name='index'),

    # FIX: Broken Access Control
    #path('note/', noteView, name='note_detail'),
    path('note/<int:note_id>/', noteView, name='note_detail'),

    path('add/', addNoteView, name='add'),
    path('delete/<int:note_id>', deleteNoteView, name='delete'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]