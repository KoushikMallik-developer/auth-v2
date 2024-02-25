import logging
from typing import Optional
from psycopg2 import DatabaseError
from rest_framework import status, serializers

from api.auth_exceptions.base_exception import AUTHBaseException


class EcomDatabaseError(AUTHBaseException, DatabaseError):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not name:
            self.name = "DatabaseError"
        else:
            self.name = name
        if not msg:
            self.msg = "Error Occurred While fetching user details"
        else:
            self.msg = msg
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


# class EcomValidationError(AUTHBaseException, ValidationError):
#     def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
#         self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
#         if not name:
#             self.name = "PydanticValidationError"
#         else:
#             self.name = name
#         if not msg:
#             self.msg = "Error Occured while converting to Pydantic object"
#         else:
#             self.msg = msg
#         super().__init__(self.name, self.msg, self.status)
#         logging.error(self.msg)


class EcomSerializerError(AUTHBaseException, serializers.ValidationError):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_400_BAD_REQUEST
        if not name:
            self.name = "SerializerValidationError"
        else:
            self.name = name
        if not msg:
            self.msg = "; ".join([error for error in self.detail])
        else:
            self.msg = msg
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class EcomValueError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_400_BAD_REQUEST
        if not name:
            self.name = "EcomValueError"
        else:
            self.name = name
        if not msg:
            self.msg = str(self)
        else:
            self.msg = msg
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class EcomDomainDoesNotExistError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_400_BAD_REQUEST
        if not name:
            self.name = "EcomDomainDoesNotExistError"
        else:
            self.name = name
        if not msg:
            self.msg = "Domain does not exists or is not responding"
        else:
            self.msg = msg
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)


class EcomValidationError(AUTHBaseException):
    def __init__(self, name: Optional[str] = None, msg: Optional[str] = None):
        self.status = status.HTTP_400_BAD_REQUEST
        if not name:
            self.name = "EcomValidationError"
        else:
            self.name = name
        if not msg:
            self.msg = "Validation Error occurred while validating user data"
        else:
            self.msg = msg
        super().__init__(self.name, self.msg, self.status)
        logging.error(self.msg)
