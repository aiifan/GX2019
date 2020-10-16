from rest_framework import viewsets  # 提供read或update之类的操作，而不是get或put等方法处理程序
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User

from .models import Snippet
from .serializers import UserSerializer, SnippetSerializer
from .permissions import IsOwnerOrReadOnly

"""
使用viewsets构建试图
"""


@api_view
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })



"""
使用ReadOnlyModelViewSet类来自动提供默认的“只读”操作。我们仍然像使用常规视图那样设置queryset和serializer_class属性，但我们不再需要向两个不同的类提供相同的信息。
"""
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    自动提供`list`和`detail`操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    此视图自动提供`list`，`create`，`retrieve`，`update`和`destroy`操作。
    另外我们还提供了一个额外的`highlight`操作。
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=True)
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
