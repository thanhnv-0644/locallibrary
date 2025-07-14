from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus, DEFAULT_PAGINATION


def index(request):
    """Hàm view cho trang chủ của website."""

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Sách có sẵn (AVAILABLE)
    num_instances_available = BookInstance.objects.filter(
        status__exact=LoanStatus.AVAILABLE.value
    ).count()
    num_authors = Author.objects.count()

    # Lấy và cập nhật số lượt truy cập
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = DEFAULT_PAGINATION


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        instances = book.bookinstance_set.all()

        # Gán class CSS tương ứng theo status
        for copy in instances:
            if copy.status == LoanStatus.AVAILABLE.value:
                copy.css_class = 'text-success'
            elif copy.status == LoanStatus.MAINTENANCE.value:
                copy.css_class = 'text-danger'
            else:
                copy.css_class = 'text-warning'

        context['book_instances'] = instances
        context['AVAILABLE'] = LoanStatus.AVAILABLE.value
        context['can_mark_returned'] = self.request.user.has_perm(
            "catalog.can_mark_returned"
        )
        return context

    def book_detail_view(self, primary_key):
        """Hàm mô phỏng xử lý FBV trong class"""
        book = get_object_or_404(Book, pk=primary_key)
        return render(
            self.request,
            'catalog/book_detail.html',
            context={'book': book}
        )
