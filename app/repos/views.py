from rest_framework.decorators import api_view, permission_classes
from .permissions import WorkerHeaderPermission
from rest_framework.response import Response
from rest_framework import status
from .serializers import RepoSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import Repo
from rest_framework import permissions
from rest_framework.views import APIView
from users.models import User


class RepoCreateUpdateView(APIView):
    permission_classes = [WorkerHeaderPermission]
    
    def post(self, request):
        """Create or update a repo"""
        repo_name = request.data.get('name')
        if not repo_name:
            return Response({
                'detail': 'Name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update if exists, otherwise create
        repo, created = Repo.objects.update_or_create(
            name=repo_name,
            defaults=request.data
        )

        serializer = RepoSerializer(repo)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


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


class FiltersListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pref_langs = [val for _, val in User.PREF_LANGS_CHOICES]
        pref_domains = [val for _, val in User.PREF_DOMAINS_CHOICES]

        return Response({
            'pref_langs': pref_langs,
            'pref_domains': pref_domains,
        })
