# app/core/exceptions.py
"""
Ampalone Partner Portal - Custom Exceptions
Version: 1.0.0
"""

from fastapi import HTTPException


class AppException(HTTPException):
    """Base application exception"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        code: str = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code or f"ERR_{status_code}"


class PartnerNotFoundException(AppException):
    def __init__(self, detail: str = "Partner not found"):
        super().__init__(status_code=404, detail=detail, code="PARTNER_NOT_FOUND")


class CustomerNotFoundException(AppException):
    def __init__(self, detail: str = "Customer not found"):
        super().__init__(status_code=404, detail=detail, code="CUSTOMER_NOT_FOUND")


class QuotationNotFoundException(AppException):
    def __init__(self, detail: str = "Quotation not found"):
        super().__init__(status_code=404, detail=detail, code="QUOTATION_NOT_FOUND")


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail, code="UNAUTHORIZED")


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail, code="FORBIDDEN")


class ValidationException(AppException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=400, detail=detail, code="VALIDATION_ERROR")
