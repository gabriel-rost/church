from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint that returns the server status.
    """
    try:
        return JsonResponse({
            "status": "healthy",
            "message": "Server is running",
        }, status=200)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({
            "status": "unhealthy",
            "message": "Server error",
        }, status=500)