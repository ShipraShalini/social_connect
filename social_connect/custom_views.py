from django.http import JsonResponse
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet


def get_status_code(response):
    for attr in ["status", "status_code"]:
        code = getattr(response, attr, None)
        if code:
            return code


class CustomCreateModelMixin(mixins.CreateModelMixin):
    """Create a model instance."""

    def create(self, request, *args, **kwargs):
        """Create an object."""
        response = super(CustomCreateModelMixin, self).create(request, *args, **kwargs)
        return JsonResponse(
            data=response.data,
            status=status.HTTP_201_CREATED,
        )


class CustomListModelMixin(mixins.ListModelMixin):
    """List a queryset."""

    def list(self, request, *args, **kwargs):
        """Retrieve a list of objects."""
        response = super(CustomListModelMixin, self).list(request, *args, **kwargs)
        return JsonResponse(data=response.data, status=get_status_code(response))


class CustomRetrieveModelMixin(mixins.RetrieveModelMixin):
    """Retrieve a model instance."""

    def retrieve(self, request, *args, **kwargs):
        """Retrieve an object."""
        response = super(CustomRetrieveModelMixin, self).retrieve(
            request, *args, **kwargs
        )
        return JsonResponse(data=response.data, status=get_status_code(response))


class CustomUpdateModelMixin(mixins.UpdateModelMixin):
    """Update a model instance."""

    def update(self, request, *args, **kwargs):
        """Update an object."""
        response = super(CustomUpdateModelMixin, self).update(request, *args, **kwargs)
        return JsonResponse(data=response.data, status=get_status_code(request))


class CustomDestroyModelMixin(mixins.DestroyModelMixin):
    """Destroy a model instance."""

    def destroy(self, request, *args, **kwargs):
        """Delete an object."""
        response = super(CustomDestroyModelMixin, self).destroy(
            request, *args, **kwargs
        )
        return JsonResponse(data=response.data, status=get_status_code(response))


class CustomModelViewSet(
    CustomCreateModelMixin,
    CustomListModelMixin,
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
    CustomDestroyModelMixin,
    GenericViewSet,
):
    pass
