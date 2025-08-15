from rest_framework import serializers
from .models import Band, BandMembership


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'name', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        user = self.context['request'].user
        band = Band.objects.create(created_by=user, **validated_data)

        BandMembership.objects.create(
            user=user,
            band=band,
            role='admin'
        )

        return band


class BandMambershipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    instruments = serializers.SerializerMethodField()

    class Meta:
        model = BandMembership
        field = [
            'id',
            'user_id',
            'name',
            'email',
            'role',
            'created_at'
        ]

    def get_name(self, obj):
        return obj.user.name

    def get_email(self, obj):
        return obj.user.email

    def get_instruments(self, obj):
        return obj.user.instruments


class BandMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandMembership
        fields = ['role']
