from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import mixins, generics

"""
使用混合(mixins)
使用基于类视图的最大优势之一是它可以轻松地创建可复用的行为。
到目前为止，我们使用的创建/获取/更新/删除操作和我们创建的任何基于模型的API视图非常相似。这些常见的行为是在REST框架的mixin类中实现的。

使用GenericAPIView构建了我们的视图，并且用上了ListModelMixin和CreateModelMixin。
基类提供核心功能，而mixin类提供.list()和.create()操作。然后我们明确地将get和post方法绑定到适当的操作。都目前为止都是显而易见的。
"""
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# 使用GenericAPIView类来提供核心功能，并添加mixins来提供.retrieve()），.update()和.destroy()操作
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)