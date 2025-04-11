from celery import shared_task
from .models import Task
from django.core.mail import send_mail
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task # test to make sure celery was running locally
def add(x, y):
    return x + y

@shared_task
def send_task_reminder(task_id, event_type): # Celery reminder
    try:
        task = Task.objects.get(id=task_id)
        user_email = task.user.email if task.user else None
        message = ''
        subject = ''

        # Dynamic messaging based on event type
        if event_type == 'created':
            subject = f"Reminder: New Task '{task.title}' Created"
            message = f"Hi, your new task '{task.title}' is due on {task.due_date.strftime('%Y-%m-%d %H:%M')}."
        elif event_type == 'completed':
            subject = f"Task Completed: '{task.title}'"
            message = f"Good job! Your task '{task.title}' was marked as completed."
        elif event_type == 'uncompleted':
            subject = f"Task Uncompleted: '{task.title}'"
            message = f"Heads up! Task '{task.title}' was marked as not completed. Don't forget to revisit it."
        elif event_type == 'flagged':
            subject = f"Urgent Task: '{task.title}'"
            message = f"Alert! Task '{task.title}' has been flagged as urgent. Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}."
        else:
            subject = f"Task Notification: '{task.title}'"
            message = f"Update regarding task: '{task.title}'"

        if user_email:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
            logger.info(f"Email sent to {user_email} for event: {event_type}")
        else:
            logger.warning(f"No email sent. User not associated with task {task_id}")

        # Prints message to console aswell for dev visibility
        print(f"[{event_type.upper()}] {message}")

    except Task.DoesNotExist: # Exception incase task ID does not exist
        logger.error(f"Task with ID {task_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to handle event '{event_type}' for task {task_id}: {e}")
