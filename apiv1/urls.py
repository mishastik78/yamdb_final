from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import SendTokenView, TokenObtainCustomView


router = DefaultRouter()
router.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/'
                'comments', views.CommentViewSet, 'comment')
router.register('titles/(?P<title_id>[0-9]+)/reviews',
                views.ReviewViewSet, 'review')
router.register('users', views.UserModelView)
router.register('titles', views.TitleView)
router.register('genres', views.GenreView)
router.register('categories', views.CategoryView)
_urlpatterns = [
    path('auth/token/', TokenObtainCustomView.as_view(),
         name='token_obtain_pair'
         ),
    path('auth/email/', SendTokenView.as_view(),
         name='token_refresh'
         ),
    path('', include(router.urls))
]
urlpatterns = [
    path('v1/', include(_urlpatterns)),
]
