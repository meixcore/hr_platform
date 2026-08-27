from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializer

class UserRegistrationView(CreateAPIView):
    permission_classes=[]
    queryset = User.objects.all()
    serializer_class = UserSerializer
