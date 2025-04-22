from rest_framework import viewsets
from .models import Dataset
from .serializers import DatasetSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        name = request.query_params.get('name')
        if name is None:
            return Response({'error': 'Debes proporcionar un nombre'}, status=400)

        dataset = Dataset.objects.filter(name=name).first()
        if not dataset:
            return Response({'error': 'Dataset no encontrado'}, status=404)

        serializer = self.get_serializer(dataset)
        return Response(serializer.data)