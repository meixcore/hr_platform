from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission

from users.models import User, Role
from resumes.models import Resume

class ResumePermissionsTest(APITestCase):

    def setUp(self):
        self.candidate_role = Role.objects.get(name="candidate")
        self.hr_role = Role.objects.get(name="hr")
        self.admin_role = Role.objects.get(name="admin")

        view_resume = Permission.objects.get(codename="view_resume")
        add_resume = Permission.objects.get(codename="add_resume")
        change_resume = Permission.objects.get(codename="change_resume")
        delete_resume = Permission.objects.get(codename="delete_resume")

        self.candidate_role.permissions.set([
            view_resume,
            add_resume,
            change_resume,
            delete_resume,
        ])

        self.hr_role.permissions.set([
            view_resume,
        ])

        self.admin_role.permissions.set([
            view_resume,
            add_resume,
            change_resume,
            delete_resume,
        ])

        self.candidate = User.objects.create_user(
            username="test_candidate",
            password="123456789",
            role=self.candidate_role,
        )

        self.other_candidate = User.objects.create_user(
            username="other_candidate",
            password="123456789",
            role=self.candidate_role,
        )

        self.candidate_resume = Resume.objects.create(
            user=self.candidate,
            position="Python Developer",
            experience="1 year",
        )

        self.other_resume = Resume.objects.create(
            user=self.other_candidate,
            position="Java Developer",
            experience="2 years",
        )

        self.hr = User.objects.create(
            username="hr",
            password="123456789",
            role=self.hr_role,
        )

        self.admin = User.objects.create(
            username="admin",
            password="123456789",
            role=self.admin_role,
        )

    def test_candidate_can_create_resume(self):
        self.client.force_authenticate(user=self.candidate)
        response = self.client.post(
            "/api/resumes/",
            {
                "position": "dev",
                "experience": "1 year",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_candidate_sees_only_own_resumes(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.get("/api/resumes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["position"],
            "Python Developer",
        )

    def test_candidate_cannot_update_other_resume(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.patch(
            f"/api/resumes/{self.other_resume.id}/",
            {
                "position": "onetwothree",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 404)

    def test_candidate_cannot_delete_resume(self):
        self.client.force_authenticate(user=self.candidate)

        response = self.client.delete(
            f"/api/resumes/{self.other_resume.id}/",

        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Resume.objects.filter(id=self.other_resume.id).exists())

    def test_hr_can_view_resume(self):
        self.client.force_authenticate(user=self.hr)

        response = self.client.get("/api/resumes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_hr_cannot_create_resume(self):
        self.client.force_authenticate(user=self.hr)

        response = self.client.post(
            "/api/resumes/",
            {
                "position": "hr",
                "experience": "1 year",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_hr_cannot_update_resume(self):
        self.client.force_authenticate(user=self.hr)

        response = self.client.patch(
            f"/api/resumes/{self.candidate_resume.id}/",
            {
                "position": "onetwothree",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_hr_cannot_delete_resume(self):
        self.client.force_authenticate(user=self.hr)

        response = self.client.delete(
            f"/api/resumes/{self.candidate_resume.id}/",

        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Resume.objects.filter(id=self.candidate_resume.id).exists())

    def test_admin_can_view_resumes(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/resumes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_admin_can_create_resume(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/resumes/",
            {
                "position": "admin",
                "experience": "5 years",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_admin_can_update_resume(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f"/api/resumes/{self.other_resume.id}/",
            {
                "position": "onetwothree",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_delete_resume(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.delete(
            f"/api/resumes/{self.candidate_resume.id}/",

        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Resume.objects.filter(id=self.candidate_resume.id).exists())