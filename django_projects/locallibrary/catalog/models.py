import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .constants import (
    LoanStatus,
    MAX_LENGTH_TITLE,
    MAX_LENGTH_NAME,
    MAX_LENGTH_SUMMARY,
    MAX_LENGTH_ISBN,
    MAX_LENGTH_IMPRINT,
    DISPLAY_GENRE_LIMIT,

)

class Genre(models.Model):
    """Model đại diện cho thể loại sách."""

    name = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        help_text=_('Nhập thể loại sách (ví dụ: Khoa học viễn tưởng)')
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model đại diện cho một cuốn sách (không phải bản sao cụ thể)."""

    title = models.CharField(max_length=MAX_LENGTH_TITLE)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=MAX_LENGTH_SUMMARY,
        help_text=_('Nhập mô tả ngắn về sách')
    )
    isbn = models.CharField(
        _('ISBN'),
        max_length=MAX_LENGTH_ISBN,
        unique=True,
        help_text=_(
            '13 ký tự (xem '
            '<a href="https://www.isbn-international.org/content/what-isbn">'
            'ISBN là gì?</a>)'
        ),
    )
    genre = models.ManyToManyField(
        'Genre',
        help_text=_('Chọn thể loại cho cuốn sách này')
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    def display_genre(self):
        """
        Creates a string for the Genre.
        This is required to display genre in Admin.
        """
        return ", ".join(
            genre.name for genre in self.genre.all()[:DISPLAY_GENRE_LIMIT]
        )
    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    """Model đại diện cho một bản sao cụ thể của sách (có thể được mượn)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('ID duy nhất cho mỗi bản sao sách trong thư viện')
    )
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=MAX_LENGTH_IMPRINT)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=[
            (
                LoanStatus.MAINTENANCE.value,
                _(LoanStatus.MAINTENANCE.name.capitalize()),
            ),
            (
                LoanStatus.ON_LOAN.value,
                _(LoanStatus.ON_LOAN.name.capitalize()),
            ),
            (
                LoanStatus.AVAILABLE.value,
                _(LoanStatus.AVAILABLE.name.capitalize()),
            ),
            (
                LoanStatus.RESERVED.value,
                _(LoanStatus.RESERVED.name.capitalize()),
            ),
        ],
        blank=True,
        default=LoanStatus.MAINTENANCE.value,
        help_text=_("Book availability"),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model đại diện cho một tác giả."""

    first_name = models.CharField(max_length=MAX_LENGTH_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Ngày mất', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Trả về URL để truy cập chi tiết tác giả này."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Chuỗi đại diện cho đối tượng Author."""
        return f'{self.last_name}, {self.first_name}'

