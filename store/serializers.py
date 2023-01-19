from rest_framework import serializers

class productSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=250)
    unit_price=serializers.DecimalField(max_digits=6,decimal_places=2)