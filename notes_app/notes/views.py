from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Note
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape


# Create your views here.

# FIX: CSFR
# Remove @csrf_exempt
@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        users = User.objects.exclude(pk=request.user.id)
        notes = Note.objects.filter(user=request.user)
        return render(request, 'notes/index.html', {'users': users, 'notes': notes})
    else:
        return redirect('login')
        

# FIX: Broken Access Control
def noteView(request, note_id):

    note = get_object_or_404(Note, pk=note_id)

    #if note.user == request.user:
        #return render(request, 'notes/note_view.html', {'note': note})
    #else:
        #return HttpResponse("You do not have permission to view this note.")
    
    return render(request, 'notes/note_view.html', {'note': note})

    ## FIX: Security Misconfiguration
        ##try:
            ##note = get_object_or_404(Note, pk=note_id)
            ##return render(request, 'notes/note_view.html', {'note': note})
        ##except:
            ##return HttpResponse("The requested note does not exist or an error occurred.")

    
    ### COMBINED FIX for the above two issues (Broken Access Control and Security Misconfiguration):
    ### Both of these error handling methods can be combined as a try-except block for better error handling
    ###try:
        ###note = get_object_or_404(Note, pk=note_id)
        ###if note.user == request.user:
            ###return render(request, 'notes/note_view.html', {'note': note})
        ###else:
            ###return HttpResponse("You do not have permission to view this note.")
    ###except:
        ###return HttpResponse("The requested note does not exist or an error occurred.")


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


# FIX: CSFR
# Remove @csrf_exempt
@csrf_exempt
@login_required
def addNoteView(request):
    # FIX: XSS
    if request.method == 'POST':
        #title = escape(request.POST.get('title', ''))
        title = request.POST.get('title', '')
        #content = escape(request.POST.get('content', ''))  # Escape user input
        content = request.POST.get('content', '')  # Vulnerable input
        note = Note.objects.create(title=title, content=content, user=request.user)
        return redirect('index')
    else:
        return render(request, 'notes/add_note.html')

# FIX: Broken Access Control
# Comment out the out commented code to fix the flaw
def deleteNoteView(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    # Checks that the user actually "owns" the note
    #if note.user == request.user:
        #note.delete()
    #else: 
        #return HttpResponse("You don't have permission to delete this note.")

    note.delete()
    return redirect('index')

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('login')