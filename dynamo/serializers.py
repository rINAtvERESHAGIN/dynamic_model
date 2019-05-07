from rest_framework import serializers


class CreateNewSchemaSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    table_fields = serializers.JSONField()


class LoggingDataSerializer(serializers.Serializer):
    data = serializers.JSONField()
    type_of = serializers.CharField(max_length=100)
    object_uuid = serializers.UUIDField()
    changed = serializers.DateField()


class RestoringObjectSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    object_uuid = serializers.UUIDField()
