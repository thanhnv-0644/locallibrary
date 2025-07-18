from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.constants import (
    LoanStatus,
    DEFAULT_PAGINATION,
    PAGINATE_BY,
    NUM_OF_WEEKS_DEFAULT,
    INITIAL_DATE_OF_DEATH,

)

import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author


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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact=LoanStatus.ON_LOAN.value)
            .order_by("due_back")
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        # Kiểm tra xem form có hợp lệ không
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(
            weeks=NUM_OF_WEEKS_DEFAULT
        )
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': INITIAL_DATE_OF_DEATH}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
