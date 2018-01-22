from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^', include('restaurants.urls')),
    url(r'^docs/', include_docs_urls(title='Restaurant API documentation')),
]