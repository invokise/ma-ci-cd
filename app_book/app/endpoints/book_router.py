from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.services.book_service import BookService
from app.models.book import Book, CreateBookRequest

book_router = APIRouter(prefix='/book', tags=['Book'])

# print()


@book_router.get('/')
def get_book(book_service: BookService = Depends(BookService)) -> list[Book]:
    print('\n///get_book///\n')
    return book_service.get_book()


@book_router.post('/')
def create_book(
        book: CreateBookRequest,
        book_service: BookService = Depends(BookService)
) -> Book:
    try:
        print('\n///post_book///\n')
        book = book_service.create_book(book.address, book.customer,
                                        book.title)
        return book.dict()
    except KeyError:
        raise HTTPException(
            400, f'Book with id={book.id} already exists')


@book_router.post('/{id}/accepted')
def accepted_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.accepted_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be activated')


@book_router.post('/{id}/pick_up')
def pick_up_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.pick_up_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be pick_up')


@book_router.post('/{id}/delivering')
def delivering_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.delivering_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be delivering')


@book_router.post('/{id}/delivered')
def delivered_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.delivered_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be delivered')


@book_router.post('/{id}/paid')
def paid_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.paid_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be paid')


@book_router.post('/{id}/done')
def done_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.done_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be done')


@book_router.post('/{id}/canceled')
def cancel_delivery(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.cancel_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Book with id={id} can\'t be canceled')


@book_router.post('/{id}/delete')
def delete_book(id: UUID, book_service: BookService = Depends(BookService)) -> Book:
    try:
        book = book_service.delete_book(id)
        return book.dict()
    except KeyError:
        raise HTTPException(404, f'Book with id={id} not found')
