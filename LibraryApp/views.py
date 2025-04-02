from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Book

def index(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'index.html', {'books': books})
    
    return HttpResponse("Metodo no permitido", status=405)

@login_required
def create_book(request):
    if request.method == 'GET':
        return render(request, 'create_book.html')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        description = request.POST.get('description')
        
        book = Book(
            title=title,
            author=author,
            published_date=published_date,
            description=description
        )
        book.save()
    
        messages.success(request, 'Libro agregado exitosamente')
        return redirect('index')
    
    return HttpResponse("Metodo no permitido",status=405)

@login_required
@require_http_methods(["DELETE"])
def delete_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return JsonResponse({'status': 'success', 'message': 'Libro eliminado exitosamente'})
    except Book.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El libro no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al eliminar el libro: {str(e)}'}, status=500)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'register.html')
            
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return render(request, 'register.html')
            
        try:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Error al crear el usuario: {str(e)}')
            return render(request, 'register.html')
            
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('index')
