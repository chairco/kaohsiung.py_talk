# boards/api_views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from boards.serializers import RecordSerializer
from boards.models import Record

import json


class DataViews(APIView):
    """
    A class based view for creating and fetching records
    """

    def get(self, request, format=None):
        """
        """
        records = Record.objects.all().order_by('-rs232_time')
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        """
        if isinstance(request.data, dict):
            data = request.data
        else:
            data = json.loads(request.data)
        
        serializer = RecordSerializer(data=data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_message, status=status.HTTP_400_BAD_REQUEST)


class DataViewsDetail(APIView):
    """
    Retrieve, update or delete a reocrd instance.
    """
    def get_object(self, factory_id):
        try:
            return Record.objects.get(pk=factory_id)
        except Record.DoesNotExist:
            raise Http404

    def get(self, request, factory_id, format=None):
        record = self.get_object(factory_id)
        serializer = RecordSerializer(record)
        return Response(serializer.data)

    def put(self, request, factory_id, format=None):
        record = self.get_object(factory_id)
        serializer = RecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, factory_id, format=None):
        record = self.get_object(factory_id)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)