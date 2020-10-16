# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Snippet
from .serializers import SnippetSerializer

# Create your views here.

"""
request.POST 只处理表单数据,只适用于'POST'方法
request.data 处理任意数据,适用于'POST'，'PUT'和'PATCH'方法,可以处理传入的json请求
return Response(data) 渲染成客户端请求的内容类型。

包装器提供了一些功能，例如确保你在视图中接收到Request实例，并将上下文添加到Response，以便可以执行内容协商。
包装器还提供了诸如在适当时候返回405 Method Not Allowed响应，并处理在使用格式错误的输入来访问request.data时发生的任何ParseError异常
@api_view装饰器  基于函数
APIView   基于类

format=None
urls-2.py 添加 from rest_framework.urlpatterns import format_suffix_patterns
为了充分利用我们的响应不再与单一内容类型连接，我们可以为API路径添加对格式后缀的支持。使用格式后缀给我们明确指定了给定格式的URL，这意味着我们的API将能够处理诸如http://example.com/api/items/4.json之类的URL
"""

@api_view(['GET','POST'])
def snippet_list(request, format=None):
    '''
    列出所有的snippet或者创建一个新的snippet
    '''
    if request.method == 'GET':
        snipper = Snippet.objects.all()
        serializer = SnippetSerializer(snipper, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    获取，更新或删除一个snippet实例
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class JSONResponse(HttpResponse):
#     """
#     将其内容呈现为JSON的HttpResponse。
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
#
# @csrf_exempt
# def snipprt_list(request):
#     """
#     列出所有的code snippet,或创建一个新的snippet
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         # 序列化
#         serializer = SnippetSerializer(snippets, many=True)
#         return JSONResponse(serializer.data)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#         return JSONResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     获取，更新或删除一个code snippet
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JSONResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return HttpResponse(status=204)
