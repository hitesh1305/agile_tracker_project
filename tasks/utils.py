from datetime import date
from .models import Task

def mark_overdue_tasks():
    today = date.today()

    overdue_tasks = Task.objects.filter(
        due_date__lt=today,
        status__in=['TODO', 'IN_PROGRESS']
    )

    for task in overdue_tasks:
        task.status = 'TODO'
        task.save()