# boards/serializers.py
from rest_framework import serializers

from boards.models import Record, Data, Device


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('id', 'measure_1', 'measure_2', )


class RecordSerializer(serializers.ModelSerializer):
    record_datas = DataSerializer(many=False)

    class Meta:
        model = Record
        fields = (
            'recordid', 'machine', 'num', 
            'rs232_time', 'record_datas'
        )

    def create(self, validated_data):
        data = validated_data.pop('record_datas')
        record = Record.objects.create(**validated_data)
        Data.objects.create(record=record, **data)
        return record
