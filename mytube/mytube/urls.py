from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about-spec'),

    path('admin/', admin.site.urls),
    path('auth/', include('Users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls')),
    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)