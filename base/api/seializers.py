from rest_framework.serializers import ModelSerializer
from base.models import Rooom

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Rooom
        fields = '__all__'