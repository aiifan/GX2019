from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import permissions # 权限设置
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User



'''
使用REST框架的reverse功能来返回完全限定的URL；第二，URL模式是通过方便的名称来标识的，我们稍后将在snippets/urls.py中声明
'''
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
通过使用mixin类，我们使用更少的代码重写了这些视图，但我们还可以再进一步。REST框架提供了一组已经混合好（mixed-in）的通用视图，我们可以使用它来简化我们的views.py模块。
"""

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    '''
    现在，如果我们创建了一个代码片段，并不能将创建该代码片段的用户与代码段实例相关联。用户不是作为序列化表示的一部分发送的，而是作为传入请求的属性。（译者注：user不在传过来的数据中，而是通过request.user获得）

我们处理的方式是在我们的代码片段视图中重写一个.perform_create()方法，这样我们可以修改实例保存的方法，并处理传入请求或请求URL中隐含的任何信息。
    '''
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


# 高亮显示
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
