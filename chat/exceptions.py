from rest_framework import exceptions, status


class CustomForbidenException(exceptions.PermissionDenied):
    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        self.detail = detail

    def __str__(self):
        return self.detail

    def get_codes(self):
        return self.detail

    def get_full_details(self):
        return self.detail


class ObjectAllreadyExists(exceptions.APIException):
    status_code = status.HTTP_202_ACCEPTED

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail

    def __str__(self):
        return self.detail

    def get_codes(self):
        return self.detail

    def get_full_details(self):
        return self.detail
