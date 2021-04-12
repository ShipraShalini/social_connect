from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from social_connect.api_response import APIResponse


def get_status_code(response):
    """Get Status code from the response."""
    for attr in ["status", "status_code"]:
        code = getattr(response, attr, None)
        if code:
            return code


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """Create a model instance."""

    def create(self, request, *args, **kwargs):
        """Create an object."""
        response = super(CustomCreateModelMixin, self).create(request, *args, **kwargs)
        return APIResponse(
            data=response.data,
            status=get_status_code(response),
            headers=response._headers,
        )


class CustomListModelMixin(mixins.ListModelMixin):
    """List a queryset."""

    def list(self, request, *args, **kwargs):
        """Retrieve a list of objects."""
        response = super(CustomListModelMixin, self).list(request, *args, **kwargs)
        return APIResponse(
            data=response.data, status=response.status_code, headers=response._headers
        )


class CustomRetrieveModelMixin(mixins.RetrieveModelMixin):
    """Retrieve a model instance."""

    def retrieve(self, request, *args, **kwargs):
        """Retrieve an object."""
        response = super(CustomRetrieveModelMixin, self).retrieve(
            request, *args, **kwargs
        )
        return APIResponse(
            data=response.data, status=response.status_code, headers=response._headers
        )


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    """Update a model instance."""

    def update(self, request, *args, **kwargs):
        """Update an object."""
        response = super(CustomUpdateModelMixin, self).update(request, *args, **kwargs)
        return APIResponse(data=response.data, status=get_status_code(response))


class CustomDestroyModelMixin(mixins.DestroyModelMixin):
    """Destroy a model instance."""

    def destroy(self, request, *args, **kwargs):
        """Delete an object."""
        response = super(CustomDestroyModelMixin, self).destroy(
            request, *args, **kwargs
        )
        return APIResponse(data=response.data, status=get_status_code(response))


class CustomModelViewSet(
    CustomCreateModelMixin,
    CustomListModelMixin,
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
    CustomDestroyModelMixin,
    GenericViewSet,
):
    pass
