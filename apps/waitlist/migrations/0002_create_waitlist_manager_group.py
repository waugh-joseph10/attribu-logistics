from django.db import migrations


def create_waitlist_manager_group(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    content_type, _ = ContentType.objects.get_or_create(
        app_label="waitlist",
        model="waitlistentry",
    )
    permissions = [
        Permission.objects.get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={"name": name},
        )[0]
        for codename, name in [
            ("view_waitlistentry", "Can view waitlist entry"),
            ("change_waitlistentry", "Can change waitlist entry"),
        ]
    ]

    group, _ = Group.objects.get_or_create(name="Waitlist Manager")
    group.permissions.add(*permissions)


def remove_waitlist_manager_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Waitlist Manager").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("waitlist", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_waitlist_manager_group, remove_waitlist_manager_group),
    ]
