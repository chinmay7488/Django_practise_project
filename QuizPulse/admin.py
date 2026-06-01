from django.contrib import admin

from .models import QuizAttempt, QuizPulseProfile, UserAnswer


@admin.register(QuizPulseProfile)
class QuizPulseProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "trivia_token_created_at", "updated_at")
    search_fields = ("user__username", "user__email", "trivia_token")
    readonly_fields = ("created_at", "updated_at")


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ("question_text", "user_selected_answer", "correct_answer", "is_correct")
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "difficulty", "score", "total_questions", "date_played")
    list_filter = ("difficulty", "category", "date_played")
    search_fields = ("user__username", "user__email", "category")
    readonly_fields = ("date_played",)
    inlines = [UserAnswerInline]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("quiz_attempt", "is_correct", "user_selected_answer", "correct_answer")
    list_filter = ("is_correct",)
    search_fields = (
        "quiz_attempt__user__username",
        "question_text",
        "user_selected_answer",
        "correct_answer",
    )
