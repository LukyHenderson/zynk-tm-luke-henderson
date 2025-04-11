from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.core.cache import cache

@receiver(user_logged_out) # clears user cache upon logout for privacy/security
def clear_user_task_cache(sender, request, user, **kwargs):
    keys = [
        f"user_{user.id}_tasks_active_all",
        f"user_{user.id}_tasks_complete_all",
    ]
    for key in keys:
        cache.delete(key)