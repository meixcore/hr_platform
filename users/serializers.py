from django.contrib.auth.models import Permission
from rest_framework import serializers
from .models import User, Role

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        role, created = Role.objects.get_or_create(name="candidate", defaults={'description':'Candidate can CRUD resume'})

        view_resume = Permission.objects.get(codename='view_resume')
        add_resume = Permission.objects.get(codename='add_resume')
        delete_resume = Permission.objects.get(codename='delete_resume')
        change_resume = Permission.objects.get(codename='change_resume')
        role.permissions.set([view_resume, add_resume, delete_resume, change_resume])

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=role,
        )

        return user