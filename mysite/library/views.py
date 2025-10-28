from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, BookInstance, Author

# Create your views here.
def index(request):
    my_context = {
        'num_books': Book.objects.count(),
        'num_authors': Author.objects.count(),
        'num_instances': BookInstance.objects.count(),
        'num_instances_available': BookInstance.objects.filter(status='a').count(),
    }
    return render(request, template_name="index.html", context=my_context)