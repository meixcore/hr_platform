from rest_framework.permissions import BasePermission, SAFE_METHODS

class ResumePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return user.has_perm("resumes.view_resume")
        elif request.method == 'POST':
            return user.has_perm("resumes.add_resume")
        elif request.method in ('PUT', 'PATCH'):
            return user.has_perm("resumes.change_resume")
        elif request.method == 'DELETE':
            return user.has_perm("resumes.delete_resume")

        return False