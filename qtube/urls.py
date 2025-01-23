# urls.py
from django.urls import path
from .views import VideoUploadView, VideoSearchView, CategoryListView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Detailed description of API endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('search/', VideoSearchView.as_view(

    ), name='video-search'),
    path('category/<int:category_id>/', CategoryListView.as_view(), name='category-videos'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
