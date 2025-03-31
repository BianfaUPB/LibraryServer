from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Book

def index(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return render(request, 'index.html', {'books': books})
    
    return HttpResponse("Metodo no permitido", status=405)

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

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('index')
