from fastapi import HTTPException
from errors.errors_details import ErrorDetail

internal_server_error = HTTPException(status_code=500,
                                      detail=ErrorDetail.INTERNAL_SERVER_ERROR)
