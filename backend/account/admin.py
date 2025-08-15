from django import forms
from django.contrib import admin
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from .models import User
from api.admin_utils import NoBulkActionsMixin
from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.html import format_html_join


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Enter password again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'instruments')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("The passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"))

    class Meta:
        model = User
        fields = (
            'email', 'name', 'username', 'instruments', 'password',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )

    def clean_password(self):
        return self.initial['password']


@admin.register(User)
class UserAdmin(NoBulkActionsMixin, BaseUserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('email', 'name', 'username', 'user_bands', 'is_staff',
                    'is_superuser', 'created_at')
    list_filter = ()
    readonly_fields = ('created_at', 'last_login')

    def user_bands(self, obj):
        bands = obj.band_memberships.values_list(
            'band__name', flat=True)
        if not bands:
            return "-"
        return ", ".join(bands)

    def has_change_permission(self, request, obj=None):
        return True

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('name', 'instruments')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Datas Importantes'), {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'username', 'instruments', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email', 'name', 'username',)
    ordering = ('-created_at',)
    filter_horizontal = ('groups', 'user_permissions',)
    user_bands.short_description = "Bands"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Credenciais inválidas")
        attrs['user'] = user
        return attrs


class GroupReadOnly(Group):
    class Meta:
        proxy = True
        verbose_name = "Group View"
        verbose_name_plural = "Groups View"


class ReadOnlyGroupAdmin(NoBulkActionsMixin, BaseGroupAdmin):
    readonly_fields = ('name', 'permissions', 'users_in_group')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Impede edição
        pass

    def users_in_group(self, obj):
        users_qs = obj.user_set.all()
        if not users_qs.exists():
            return "-"
        return format_html_join(
            '',
            '<a href="{}">{}</a> <br>',
            (
                (
                    reverse(
                        f"admin:{u._meta.app_label}_user_change", args=[u.id]),
                    u.username
                )
                for u in users_qs
            )
        )
    users_in_group.short_description = _("Users in this group")

    fieldsets = (
        (None, {'fields': ('name', 'permissions', 'users_in_group')}),
    )


class EditableGroupAdmin(NoBulkActionsMixin, BaseGroupAdmin):
    filter_horizontal = ('permissions',)


admin.site.unregister(Group)
admin.site.register(Group, EditableGroupAdmin)
admin.site.register(GroupReadOnly, ReadOnlyGroupAdmin)
