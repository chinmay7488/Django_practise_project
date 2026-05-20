from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class AnalyzeSave(models.Model):
    Person = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.TextField(max_length=100)
    orginal_text = models.TextField()
    updated_text = models.TextField()
    words_count  = models.IntegerField()
    sentence_count =  models.IntegerField()
    character_count =  models.IntegerField()
    paragraph_count =  models.IntegerField()
    readablity_score = models.IntegerField()
    reading_time = models.FloatField()
    Saving_date_time = models.DateTimeField(auto_now_add=True)

