from rest_framework import serializers


class ObjectsCountsSerializer(serializers.Serializer):
    value = serializers.CharField(read_only=True)
    count = serializers.IntegerField(read_only=True)


class IntegerSumSerializer(serializers.Serializer):
    sum = serializers.IntegerField(read_only=True)


class DecimalSumSerializer(serializers.Serializer):
    sum = serializers.DecimalField(read_only=True, max_digits=11, decimal_places=2)
