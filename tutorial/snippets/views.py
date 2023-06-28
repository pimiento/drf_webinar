from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from django.http import JsonResponse

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer

class ListSnippets(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response("Created new post", status=status.HTTP_201_CREATED)


class SnippetsListUser(generics.ListAPIView):
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Snippet.objects.filter(owner=user)

class SnippetsListUserKwargs(generics.ListAPIView):
    serializer_class = SnippetSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Snippet.objects.filter(owner__username=username)

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly, )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        return SnippetSerializer

    # def check_permissions(self, request):
    #     print(self.get_permissions())
    #     super().check_permissions(request)
    #     print("Checking permissions request based")
    #     # self.permission_denied(
    #     #             request,
    #     #             message="Not allowed 🤷🏻‍♀️"
    #     #         )

    # def check_object_permissions(self, request, obj):
    #     print("Now checking object permissions")
    #     super().check_object_permissions(request, obj)
    #     # self.permission_denied(
    #     #             request,
    #     #             message="Not allowed 🤷🏻‍♀️ 🤷🏻‍♀️"
    #     #         )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
