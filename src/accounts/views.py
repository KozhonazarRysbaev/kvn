import json

from django.http import Http404
from django.db.models import Sum, Q
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from accounts.filters import UserFilter
from accounts.serializers import UserSerializer, UserUpdateSerializer, PostUserSerializer, RatingUser, \
    UserCreateSerializer, ChangePasswordSerializer, UserCrystalSerializer, ProfessionSerializer, \
    ProfessionUserSerializer
from accounts.models import User, Profession
from accounts.permissions import IsSelf
from social.models import Post
from billing.models import CrystalTransaction


class UserViewSet(viewsets.ModelViewSet, PageNumberPagination):
    """
        retrieve:
            Return a user instance

        list:
            Return all users, ordered by most recently joined.

        create:
            Create a new user.

        partial_update:
            Update one or more fields on an existing user, only owner is available.

        update:
           Update user, only owner is available

        rating:
            List of Users with crystals

        donation:
            Donation for user post parameter amount

        """
    queryset = User.objects.order_by('-crystals')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]
    filter_class = UserFilter
    http_method_names = ('get', 'head', 'options', 'post', 'put', 'patch')

    @action(detail=False, permission_classes=[])
    def rating(self, request):
        users = User.objects.annotate(crystals=Sum('transactions__amount')).order_by('-crystals')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserCrystalSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAuthenticated], methods=['post'])
    def donation(self, request, pk):
        if request.content_type == 'application/json':
            amount = json.loads(request.body.decode('utf-8')).get('amount')
        else:
            amount = request.POST.get('amount')
        if not amount:
            return Response({'success': False, 'message': 'amount required field'})
        user_balanse = request.user.get_balance()
        to_user = self.get_object()
        if user_balanse and user_balanse >= int(amount):
            with transaction.atomic():
                CrystalTransaction.objects.create(user=request.user, amount=amount, content_object=to_user,
                                                  action='cash_out')
                CrystalTransaction.objects.create(user=to_user, amount=amount, content_object=request.user,
                                                  action='cash_in')
        else:
            return Response({'success': False, 'message': 'Не достаточно кристалов'}, status=403)
        return Response({'success': True, 'message': 'Вы успешно перевели койны'})

    def get_permissions(self):
        if self.action in ('create', 'list', 'retrieve'):
            self.permission_classes = ()
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            self.serializer_class = UserUpdateSerializer
        elif self.action == 'create':
            self.serializer_class = UserCreateSerializer
        return super().get_serializer_class()


class UserPostViewSet(viewsets.ModelViewSet):
    """
       retrieve:
           Not work, return 404 Not Found

       list:
           Return all posts by user
    """
    serializer_class = PostUserSerializer
    permission_classes = [AllowAny]
    http_method_names = ('get', 'head', 'options')

    def retrieve(self, request, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        return Post.objects.filter(user_id=self.kwargs['user_pk'])


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    http_method_names = ('put',)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionViewSet(viewsets.ModelViewSet):
    """
       retrieve:
           Return instance object profession

       list:
           Return all professions
    """
    http_method_names = ('get', 'head', 'options',)
    permission_classes = (AllowAny,)
    serializer_class = ProfessionSerializer
    queryset = Profession.objects.all()


class ProfessionUserViewSet(viewsets.ModelViewSet):
    """
    list:
        Return all user profession
    retrieve:
           Not work, return 404 Not Found
    """
    serializer_class = ProfessionUserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ('get', 'head', 'options')

    def retrieve(self, request, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        return User.objects.filter(profession__id=self.kwargs['profession_pk'])
