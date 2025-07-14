from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus


def index(request):
    """Hàm view cho trang chủ của website."""

    # Tạo thống kê số lượng cho một số đối tượng chính
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    
    # Sách có sẵn (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status=LoanStatus.AVAILABLE.value
    )

# Hàm all() được ngầm định mặc định
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

# Trả về file HTML template index.html với dữ liệu trong biến context
    return render(request, 'index.html', context=context)
