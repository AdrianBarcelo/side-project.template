import json

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from template.shared.domain.exceptions.domain_exception import DomainException
from template.shared.domain.exceptions.not_found import NotFound


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except NotFound as error:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=json.dumps({"error": error.error_message()}),
            )
        except DomainException as error:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps({"error": error.error_message()}),
            )
