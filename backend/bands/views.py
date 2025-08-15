
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Band, BandMembership
from .serializers import BandSerializer, BandMambershipSerializer, BandMemberUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class CreateBandView(generics.CreateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        BandMembership.objects.create(
            Band=band, user=self.request.user, role='admin')


class ListBandMembersView(generics.ListAPIView):
    serializer_class = BandMambershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        band_id = self.kwargs['band_id']
        user = self.request.user

        if not BandMembership.objects.filter(band_id=band_id, user=user).exists():
            raise PermissionDenied("You are not part of this Band.")

        return BandMembership.objects.filter(band_id=band_id).select_related('user', 'Band')


class AddMemberView(generics.CreateAPIView):
    serializer_class = BandMambershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        band = serializer.validated_data['band']
        if not BandMembership.objects.filter(band=band, user=self.request.user, role='admin').exists():
            raise PermissionDenied("Only administrators can add members.")

        user = serializer.validated_data['user']
        if BandMembership.objects.filter(band=band, user=user).exists():
            raise ValidationError("Usuário já é membro do grupo.")

        serializer.save()


class RemoveMemberView(APIView):
    def delete(self, request, band_id, user_id):
        if not BandMembership.objects.filter(band_id=band_id, user=request.user, role='admin').exists():
            raise PermissionDenied(
                "Apenas administradores podem remover membros.")

        membership = get_object_or_404(
            BandMembership, band_id=band_id, user_id=user_id)

        if membership.user == request.user:
            raise ValidationError("Você não pode se remover do grupo.")

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateMemberRoleView(generics.UpdateAPIView):
    serializer_class = BandMemberUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Band__memberships__user=self.request.user, Band__memberships__role='admin')
