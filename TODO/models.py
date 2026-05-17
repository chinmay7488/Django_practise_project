from django.db import models

# Create your models here.
class TaskDetails(models.Model):
    Priority_choices={
        ('H', 'high'),
        ('M', 'Medium'),
        ('L', 'Low')
    }

    Title = models.CharField(max_length=150)
    Description = models.TextField()
    Created_At = models.DateTimeField(auto_now_add=True)
    Due_Date = models.DateTimeField()
    Is_Completed = models.BooleanField(default=False)
    Priority = models.CharField(max_length=1, choices=Priority_choices, default='M')