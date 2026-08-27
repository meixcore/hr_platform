from rest_framework import viewsets
from .models import Resume
from .serializers import ResumeSerializer
from .permissions import ResumePermission

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [ResumePermission]

    def get_queryset(self):
        if self.request.user.role.name == 'candidate':
            return Resume.objects.filter(user=self.request.user)
        return Resume.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
