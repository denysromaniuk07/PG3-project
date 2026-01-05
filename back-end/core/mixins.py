from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class OwnerFilterMixin:
    """
    Mixin that filters queryset by owner (current user).
    Assumes model has a 'user' or 'author' field.
    """
    owner_field = 'user'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            filter_kwargs = {self.owner_field: self.request.user}
            return queryset.filter(**filter_kwargs)
        return queryset.none()


class CreateUserMixin:
    """
    Mixin that automatically sets the current user when creating objects.
    Assumes model has a 'user' or 'author' field.
    """
    user_field = 'user'

    def perform_create(self, serializer):
        kwargs = {self.user_field: self.request.user}
        serializer.save(**kwargs)


class UpdateTimestampMixin:
    """Mixin that updates timestamps on modification"""
    
    def perform_update(self, serializer):
        serializer.save(updated_at=serializer.instance.updated_at)


class LikeDislikeMixin:
    """
    Mixin to handle like/dislike functionality.
    Subclass must implement get_object() and have a model with likes_count.
    """
    
    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        """Like an object"""
        obj = self.get_object()
        obj.likes_count = (obj.likes_count or 0) + 1
        obj.save()
        return Response({
            'status': 'liked',
            'likes_count': obj.likes_count
        })

    @action(detail=True, methods=['post'])
    def unlike(self, request, *args, **kwargs):
        """Unlike an object"""
        obj = self.get_object()
        if obj.likes_count > 0:
            obj.likes_count -= 1
            obj.save()
        return Response({
            'status': 'unliked',
            'likes_count': obj.likes_count
        })


class BulkActionMixin:
    """
    Mixin to support bulk operations (delete, update status, etc.)
    """
    
    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """Delete multiple objects"""
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'error': 'No IDs provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count, _ = self.get_queryset().filter(id__in=ids).delete()
        return Response({
            'status': 'deleted',
            'deleted_count': deleted_count
        })

    @action(detail=False, methods=['post'])
    def bulk_update_status(self, request):
        """Update status for multiple objects"""
        ids = request.data.get('ids', [])
        new_status = request.data.get('status')
        
        if not ids or not new_status:
            return Response(
                {'error': 'IDs and status required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated_count = self.get_queryset().filter(
            id__in=ids
        ).update(status=new_status)
        
        return Response({
            'status': 'updated',
            'updated_count': updated_count
        })


class SearchFilterMixin:
    """
    Mixin to add advanced search and filtering capabilities.
    Configure search_fields and filterset_fields in ViewSet.
    """
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search')
        
        if search_term and hasattr(self, 'search_fields'):
            from django.db.models import Q
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': search_term})
            queryset = queryset.filter(q_objects)
        
        return queryset


class ExportMixin:
    """Mixin to support data export (CSV, JSON)"""
    
    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export data in requested format"""
        format_type = request.query_params.get('format', 'json')
        queryset = self.get_queryset()
        
        if format_type == 'csv':
            return self._export_csv(queryset)
        elif format_type == 'json':
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Unsupported format'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def _export_csv(self, queryset):
        """Export queryset as CSV"""
        import csv
        from django.http import HttpResponse
        
        serializer = self.get_serializer(queryset, many=True)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        
        if not serializer.data:
            return response
        
        writer = csv.DictWriter(response, fieldnames=serializer.data[0].keys())
        writer.writeheader()
        writer.writerows(serializer.data)
        
        return response


class SoftDeleteMixin:
    """Mixin for soft-delete functionality"""
    
    @action(detail=True, methods=['post'])
    def soft_delete(self, request, *args, **kwargs):
        """Soft delete an object"""
        obj = self.get_object()
        obj.soft_delete()
        return Response({'status': 'deleted'})

    @action(detail=True, methods=['post'])
    def restore(self, request, *args, **kwargs):
        """Restore a soft-deleted object"""
        obj = self.get_object()
        obj.restore()
        return Response({'status': 'restored'})


class NestedRouterMixin:
    """
    Mixin to handle nested routes (e.g., /users/1/skills/).
    Configure parent_lookup_field in ViewSet.
    """
    parent_lookup_field = 'parent_id'
    parent_lookup_url_kwarg = 'parent_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        parent_id = self.kwargs.get(self.parent_lookup_url_kwarg)
        
        if parent_id:
            filter_kwargs = {f'{self.parent_lookup_field}': parent_id}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset
