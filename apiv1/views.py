from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from . import serializers
from .filters import GenreFilter
from .models import Category, Genre, Review, Title
from .permissions import (IsAuthorOrAbovePermission, IsModelAdminPermission,
                          IsSafeOrAdminPermission)

User = get_user_model()


class SendTokenView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.SendTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(username=serializer.validated_data['email'])
        user = get_object_or_404(User, email=serializer.data['email'])
        token = default_token_generator.make_token(user)
        user.confirmation_code = token
        user.save()
        send_mail(
            'Confirmation code',
            f'Confirmation code is {token}',
            settings.EMAIL_FROM_ADDRESS,
            [user.email],
            fail_silently=False,
        )


class TokenObtainCustomView(TokenViewBase):
    serializer_class = serializers.TokenObtainCustomSerializer


class UserModelView(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-pk')
    serializer_class = serializers.UserModelViewSerializer
    permission_classes = (IsModelAdminPermission,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            url_path='me', methods=['get', 'patch'])
    def user_profile_edit(self, request):
        serializer = self.get_serializer(self.request.user,
                                         data=request.data,
                                         partial=True
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrAbovePermission)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(
                            Title,
                            pk=self.kwargs['title_id']
                        )
                        )


class CommentViewSet(ReviewViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        review = get_object_or_404(queryset, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=get_object_or_404(
                            Review,
                            pk=self.kwargs['review_id']
                        )
                        )


class TitleView(viewsets.ModelViewSet):
    queryset = Title.objects.order_by('-pk').annotate(
        rating=Avg('reviews__score'))
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsSafeOrAdminPermission, permissions.AllowAny)
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = GenreFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleRetrieveSerializer
        return serializers.TitleSerializer


class CategoryView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Category.objects.order_by('-pk')
    serializer_class = serializers.CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsSafeOrAdminPermission, permissions.AllowAny)
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class GenreView(CategoryView):
    """
    Наследуемся от категорий, функционал идентичен
    """
    queryset = Genre.objects.order_by('-pk')
    serializer_class = serializers.GenreSerializer
