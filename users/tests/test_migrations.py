from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

class CreateRolesMigration(TransactionTestCase):

    migrate_from = ("users", "0002_alter_user_role")
    migrate_to = ("users", "0003_create_roles")

    def setUp(self):
        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_from])
        self.executor = MigrationExecutor(connection)
        self.executor.migrate([self.migrate_to])
        self.apps = self.executor.loader.project_state([self.migrate_to]).apps

    def test_roles_exists(self):
        Role = self.apps.get_model("users", "Role")

        self.assertTrue(Role.objects.filter(name="candidate").exists())
        self.assertTrue(Role.objects.filter(name="hr").exists())
        self.assertTrue(Role.objects.filter(name="admin").exists())

    def test_roles_have_correct_permissions(self):
        Role = self.apps.get_model("users", "Role")

        candidate = Role.objects.get(name="candidate")
        hr = Role.objects.get(name="hr")
        admin = Role.objects.get(name="admin")

        candidate_permissions = set(candidate.permissions.values_list("codename", flat=True))
        hr_permissions = set(hr.permissions.values_list("codename", flat=True))
        admin_permissions = set(admin.permissions.values_list("codename", flat=True))

        self.assertEqual(
            candidate_permissions,
            {
                "view_resume",
                "add_resume",
                "change_resume",
                "delete_resume",
            }
        )

        self.assertEqual(
            hr_permissions,
            {"view_resume",}
        )

        self.assertEqual(
            admin_permissions,
            {
                "view_resume",
                "add_resume",
                "change_resume",
                "delete_resume",
            }
        )