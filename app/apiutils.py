"""APIUtils implementation for Django REST Framework APIs."""
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, TypeVar

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response as DRFResponse
from rest_framework.serializers import Serializer

T = TypeVar("T")


class Error:
    """Error information for API responses."""

    def __init__(
        self, message: str, code: Optional[str] = None, num_code: Optional[int] = None
    ):
        self.message = message
        self.code = code
        self.num_code = num_code

    def to_dict(self) -> Dict:
        return {"message": self.message, "code": self.code, "num_code": self.num_code}


@dataclass
class PagingLinks:
    """Paging links for collection responses."""

    first: Optional[str] = None
    previous: Optional[str] = None
    next: Optional[str] = None
    last: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "first": self.first,
            "previous": self.previous,
            "next": self.next,
            "last": self.last,
        }


@dataclass
class Paging:
    """Paging information for collection responses."""

    page: Optional[int] = None
    items: Optional[int] = None
    total_pages: Optional[int] = None
    total_items: Optional[int] = None
    links: Optional[PagingLinks] = None

    def to_dict(self) -> Dict:
        return {
            "page": self.page,
            "items": self.items,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "links": self.links.to_dict() if self.links else None,
        }


class CustomPagination(PageNumberPagination):
    """Custom pagination class that works with our response format."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "data": schema,
                "paging": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "nullable": True},
                        "items": {"type": "integer", "nullable": True},
                        "total_pages": {"type": "integer", "nullable": True},
                        "total_items": {"type": "integer", "nullable": True},
                        "links": {
                            "type": "object",
                            "properties": {
                                "first": {"type": "string", "nullable": True},
                                "previous": {"type": "string", "nullable": True},
                                "next": {"type": "string", "nullable": True},
                                "last": {"type": "string", "nullable": True},
                            },
                        },
                    },
                },
                "errors": {
                    "type": "array",
                    "items": {"type": "object"},
                    "nullable": True,
                },
                "info": {"type": "object", "nullable": True},
            },
        }

    def get_paginated_response(self, data):
        return CollectionResponse(
            data=data,
            paging=Paging(
                page=self.page.number,
                items=len(data),
                total_pages=self.page.paginator.num_pages,
                total_items=self.page.paginator.count,
                links=PagingLinks(
                    # TODO: Implement self.get_first_link()
                    first=None,
                    previous=self.get_previous_link(),
                    next=self.get_next_link(),
                    # TODO: Implement self.get_last_link()
                    last=None,
                ),
            ),
        ).to_response()


class BaseResponseMixin:
    """Base mixin for all response classes."""

    def __init__(
        self,
        errors: Optional[List[Error]] = None,
        info: Optional[Dict] = None,
        **kwargs
    ):
        self.errors = errors
        self.info = info
        super().__init__(**kwargs)

    def to_response(self) -> DRFResponse:
        data = {}
        if hasattr(self, "errors") and self.errors:
            data["errors"] = [error.to_dict() for error in self.errors]
        if hasattr(self, "info") and self.info:
            data["info"] = self.info
        return DRFResponse(data)


class Response(BaseResponseMixin, Generic[T]):
    """Single object response wrapper."""

    def __init__(
        self, obj: Optional[T] = None, serializer: Optional[Serializer] = None, **kwargs
    ):
        self.object = obj
        self.serializer = serializer
        super().__init__(**kwargs)

    def to_response(self) -> DRFResponse:
        data = super().to_response().data
        if self.object is not None:
            if self.serializer:
                data["object"] = self.serializer.data
            else:
                data["object"] = self.object
        return DRFResponse(data)


class CollectionResponse(BaseResponseMixin, Generic[T]):
    """Collection response wrapper."""

    def __init__(
        self,
        data: Optional[List[T]] = None,
        serializer: Optional[Serializer] = None,
        paging: Optional[Paging] = None,
        **kwargs
    ):
        self.data = data
        self.serializer = serializer
        self.paging = paging
        super().__init__(**kwargs)

    def to_response(self) -> DRFResponse:
        data = super().to_response().data
        if self.data is not None:
            if self.serializer:
                data["data"] = self.serializer.data
            else:
                data["data"] = self.data
        if self.paging:
            data["paging"] = self.paging.to_dict()
        return DRFResponse(data)


class APIUtilsViewSet(viewsets.ModelViewSet):
    """Base viewset for APIUtils views."""

    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(obj=serializer.data).to_response()
