from rest_framework import serializers

class FormInputSerializer(serializers.Serializer):
    data = serializers.DictField(child=serializers.CharField(), required=True)
