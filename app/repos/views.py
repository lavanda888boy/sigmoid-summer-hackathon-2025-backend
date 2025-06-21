from rest_framework.decorators import api_view, permission_classes
from .permissions import WorkerHeaderPermission
from rest_framework.response import Response
from rest_framework import status
from .serializers import RepoSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import Repo
from rest_framework import permissions


@api_view(['POST'])
@permission_classes([WorkerHeaderPermission])
def create_repo(request):
    serializer = RepoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepoSearchPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'


class RepoSearchView(ListAPIView):
    serializer_class = RepoSerializer
    pagination_class = RepoSearchPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Repo.objects.all()

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        langs = self.request.query_params.getlist('lang')
        if langs:
            queryset = queryset.filter(langs__overlap=langs)

        domains = self.request.query_params.getlist('domain')
        if domains:
            queryset = queryset.filter(domains__overlap=domains)

        good_first = self.request.query_params.get('good_first', '')
        good_first = good_first.lower() in ['true', '1', 'yes']
        if good_first:
            queryset = queryset.filter(good_first=True)

        return queryset
