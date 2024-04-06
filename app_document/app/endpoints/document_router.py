from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.services.document_service import DocumentService
from app.models.document import Document, CreateDocumentRequest

document_router = APIRouter(prefix='/document', tags=['Document'])


@document_router.get('/')
def get_document(document_service: DocumentService = Depends(DocumentService)) -> list[Document]:
    return document_service.get_document()


@document_router.post('/')
def create_document(
        document: CreateDocumentRequest,
        documnet_service: DocumentService = Depends(DocumentService)
) -> Document:
    try:
        document = documnet_service.create_document(document.book_id, document.doc,
                                                    document.customer)

        return document.dict()
    except KeyError:
        raise HTTPException(
            400, f'Document with id={document.id} already exists')


@document_router.post('/{id}/delete')
def delete_document(id: UUID, document_service: DocumentService = Depends(DocumentService)) -> Document:
    try:
        document = document_service.delete_document(id)
        return document
    except KeyError:
        raise HTTPException(404, f'Document with id={id} not found')
