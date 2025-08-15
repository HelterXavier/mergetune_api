from django.urls import path
from .views import (
    CreateBandView,
    ListBandMembersView,
    AddMemberView,
    RemoveMemberView,
    UpdateMemberRoleView,
)

urlspatters = [
    path('bands/create/', CreateBandView.as_view(), name='create-band'),
    path('bands/<int:band_id>/members/',
         ListBandMembersView.as_view(), name='list-members'),
    path('bands/<int:band_id>/add_members/',
         AddMemberView.as_view(), name='add-member'),
    path('bands/<int:band_id>/members/<int:user_id>/remove/',
         RemoveMemberView.as_view(), name='remove-member'),
    path('bands/members/<int:pk>/update/',
         UpdateMemberRoleView.as_view(), name='update-member-role'),
]
