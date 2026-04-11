from django.contrib.auth import get_user_model


def get_demo_user():
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(
        username="demo_collector",
        defaults={"coins": 0},
    )
    return user
