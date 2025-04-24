import pandas as pd
from rest_framework import viewsets
from .models import Dataset
from .serializers import DatasetSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from data_insights_cli.analyzer.stats import analyze_csv, sanitize_for_json
from data_insights_cli.analyzer.predictor import predict_values
import os

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
    
class DatasetAnalysisView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        file_path = dataset.file.path
        if not os.path.exists(file_path):
            return Response({"error": "Archivo no encontrado en el servidor."}, status=status.HTTP_404_NOT_FOUND)

        with open(file_path, 'rb') as f:
            analysis = analyze_csv(f.read())

        sanitized_analysis = sanitize_for_json(analysis)

        return Response(sanitized_analysis)
    
class PredictView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({"error": "Dataset no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        file_path = dataset.file.path
        if not os.path.exists(file_path):
            return Response({"error": "Archivo no encontrado en el servidor."}, status=status.HTTP_404_NOT_FOUND)

        df = pd.read_csv(file_path)
        feature = request.query_params.get("feature")
        target = request.query_params.get("target")
        future_vals = request.query_params.getlist("future", type=float)

        if not feature or not target or not future_vals:
            return Response({"error": "Parámetros 'feature', 'target' y 'future' son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            resultado = predict_values(df, feature, target, future_vals)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "feature": feature,
            "target": target,
            "predicciones": [{"x": x, "y": y} for x, y in resultado]
        })