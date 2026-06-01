from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class QuizPulseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="quizpulse_profile")
    trivia_token = models.CharField(max_length=255, blank=True)
    trivia_token_created_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save_trivia_token(self, token):
        self.trivia_token = token
        self.trivia_token_created_at = timezone.now()
        self.save(update_fields=["trivia_token", "trivia_token_created_at", "updated_at"])

    def __str__(self):
        return f"{self.user.username} QuizPulse profile"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    category = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=20)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    date_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_played"]

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.score}/{self.total_questions})"


class UserAnswer(models.Model):
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question_text = models.TextField()
    user_selected_answer = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz_attempt.user.username} - {'Correct' if self.is_correct else 'Incorrect'}"


@receiver(post_save, sender=User)
def create_quizpulse_profile(sender, instance, created, **kwargs):
    if created:
        QuizPulseProfile.objects.get_or_create(user=instance)
