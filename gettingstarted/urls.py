from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from django.views.generic import TemplateView
from mailroom.views import UploadDataView

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'profile.html')),
    path('uploaded/', UploadDataView.as_view(), name = 'uploaded'),
    path("admin/", admin.site.urls),
]
