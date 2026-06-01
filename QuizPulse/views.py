from html import unescape
from random import shuffle
from time import time
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .models import QuizAttempt, QuizPulseProfile, UserAnswer


PASS_PERCENTAGE = 70
TIME_LIMIT_MINUTES = 10
CATEGORIES = {}

Questions_url='https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={diff}&type={type}&token={token}'
Token_url='https://opentdb.com/api_token.php?command=request'
ResetToken_url='https://opentdb.com/api_token.php?command=reset&token={token}'


def login_page(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "QuizPulse:home"

    if request.user.is_authenticated:
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("QuizPulse:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not request_trivia_token(user):
                messages.warning(request, "Logged in, but the quiz token could not be refreshed right now.")
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("QuizPulse:home")

        messages.error(request, "Invalid username or password.")

    return render(request, "QuizPulse/login.html", {"next": next_url})
def register_page(request):
    if request.user.is_authenticated:
        return redirect("QuizPulse:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            if not request_trivia_token(user):
                messages.warning(request, "Account created, but the quiz token could not be created right now.")
            return redirect("QuizPulse:home")

    return render(request, "QuizPulse/register.html")
def logout_page(request):
    logout(request)
    return redirect("QuizPulse:login")
def request_trivia_token(user):
    profile, _ = QuizPulseProfile.objects.get_or_create(user=user)

    try:
        print('inside request_trivia_token')
        response = requests.get(Token_url, timeout=5)
        response.raise_for_status()
        token = response.json().get("token")
    except (requests.RequestException, ValueError):
        return None

    if not token:
        return None

    profile.save_trivia_token(token)
    return token
def get_trivia_token(user):
    profile, _ = QuizPulseProfile.objects.get_or_create(user=user)

    if profile.trivia_token:
        return profile.trivia_token

    return request_trivia_token(user)


def GetCategories():
    url = 'https://opentdb.com/api_category.php'
    response = requests.get(url).json()['trivia_categories']
    for res in response:
        CATEGORIES[res['id']] = res['name']
        
def fetch_quiz_questions(amount, category, difficulty, question_type, token):
    url = Questions_url.format(
        amount=amount,
        category=category,
        diff=difficulty,
        type=question_type,
        token=token,
    )

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return []

    if payload.get("response_code") == 4:
        return None

    if payload.get("response_code") != 0:
        return []

    questions = []
    for index, item in enumerate(payload.get("results", []), start=1):
        correct_answer = unescape(item["correct_answer"])
        choices = [correct_answer]
        choices.extend(unescape(answer) for answer in item["incorrect_answers"])
        shuffle(choices)

        questions.append(
            {
                "id": index,
                "category": unescape(item["category"]),
                "difficulty": item["difficulty"],
                "type": item["type"],
                "question": unescape(item["question"]),
                "choices": choices,
                "answer": correct_answer,
            }
        )

    return questions

def home(request):
    if not CATEGORIES:
        GetCategories()
    return render(
        request,
        "QuizPulse/home.html",
        {
            "categories": CATEGORIES,
            "difficulties": ["easy", "medium", "hard"],
            "question_types": [("multiple", "Multiple Choice"), ("boolean", "True / False")],
        },
    )


@login_required(login_url="QuizPulse:login")
def start_quiz(request):
    if request.method != "POST":
        return redirect("QuizPulse:home")

    token = get_trivia_token(request.user)
    if not token:
        messages.error(request, "Could not create a quiz token. Please try logging in again.")
        return redirect("QuizPulse:home")

    amount = int(request.POST.get("amount", 10))
    category = request.POST.get("category")
    difficulty = request.POST.get("difficulty")
    question_type = request.POST.get("question_type")

    questions = fetch_quiz_questions(amount, category, difficulty, question_type, token)

    if questions is None or len(questions) == 0:
        token = request_trivia_token(request.user)
        if token:
            questions = fetch_quiz_questions(amount, category, difficulty, question_type, token)

    if not questions:
        messages.error(request, "Could not load quiz questions right now. Please try again.")
        return redirect("QuizPulse:home")

    quiz_attempt = QuizAttempt.objects.create(
        user=request.user,
        category=questions[0]["category"],
        difficulty=difficulty,
        total_questions=len(questions),
    )

    request.session["quiz_questions"] = questions
    request.session["quiz_attempt_id"] = quiz_attempt.id
    request.session["current_question_index"] = 0
    request.session["answers"] = {}
    request.session["score"] = 0
    request.session["started_at"] = time()
    request.session["time_limit_seconds"] = TIME_LIMIT_MINUTES * 60
    request.session.modified = True

    return redirect("QuizPulse:question")


@login_required(login_url="QuizPulse:login")
def question(request):
    questions = request.session.get("quiz_questions")
    current_index = request.session.get("current_question_index", 0)

    if not questions:
        return redirect("QuizPulse:home")

    if _time_expired(request):
        return redirect("QuizPulse:results")

    if current_index >= len(questions):
        return redirect("QuizPulse:results")

    current_question = questions[current_index]

    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        answers = request.session.get("answers", {})

        if selected_answer:
            is_correct = selected_answer == current_question["answer"]
            answers[str(current_question["id"])] = {
                "selected": selected_answer,
                "is_correct": is_correct,
            }
            request.session["answers"] = answers
            request.session["score"] = sum(1 for answer in answers.values() if answer["is_correct"])

        request.session["current_question_index"] = current_index + 1
        request.session.modified = True

        if current_index + 1 >= len(questions):
            return redirect("QuizPulse:results")
        return redirect("QuizPulse:question")

    return render(
        request,
        "QuizPulse/question.html",
        {
            "question": current_question,
            "question_number": current_index + 1,
            "total_questions": len(questions),
            "is_last_question": current_index + 1 == len(questions),
            "remaining_seconds": _remaining_seconds(request),
        },
    )


@login_required(login_url="QuizPulse:login")
def results(request):
    questions = request.session.get("quiz_questions", [])
    answers = request.session.get("answers", {})
    score = sum(1 for answer in answers.values() if answer["is_correct"])
    total_questions = len(questions)
    percentage = round((score / total_questions) * 100) if total_questions else 0
    passed = percentage >= PASS_PERCENTAGE
    timed_out = _time_expired(request)

    _save_quiz_attempt(request, questions, answers, score, total_questions)

    request.session["score"] = score
    request.session["percentage"] = percentage
    request.session["passed"] = passed
    request.session["timed_out"] = timed_out
    request.session.modified = True

    return render(
        request,
        "QuizPulse/results.html",
        {
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "passed": passed,
            "pass_percentage": PASS_PERCENTAGE,
            "timed_out": timed_out,
        },
    )


@login_required(login_url="QuizPulse:login")
def review(request, attempt_id=None):
    attempts = QuizAttempt.objects.filter(user=request.user).prefetch_related("answers")
    selected_attempt = None
    review_items = []

    if attempt_id:
        selected_attempt = get_object_or_404(attempts, id=attempt_id)
    elif attempts:
        selected_attempt = attempts.first()

    if selected_attempt:
        review_items = selected_attempt.answers.all()

    return render(
        request,
        "QuizPulse/review.html",
        {
            "attempts": attempts,
            "selected_attempt": selected_attempt,
            "review_items": review_items,
        },
    )


@login_required(login_url="QuizPulse:login")
def delete_attempt(request, attempt_id):
    quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

    if request.method == "POST":
        if request.session.get("quiz_attempt_id") == quiz_attempt.id:
            request.session.pop("quiz_attempt_id", None)
            request.session.modified = True
        quiz_attempt.delete()
        messages.success(request, "Quiz attempt deleted.")

    return redirect("QuizPulse:review")


@login_required(login_url="QuizPulse:login")
def restart(request):
    for key in [
        "quiz_questions",
        "quiz_attempt_id",
        "current_question_index",
        "answers",
        "score",
        "started_at",
        "time_limit_seconds",
        "percentage",
        "passed",
        "timed_out",
    ]:
        request.session.pop(key, None)

    return redirect("QuizPulse:home")

def _remaining_seconds(request):
    started_at = request.session.get("started_at", time())
    time_limit_seconds = request.session.get("time_limit_seconds", TIME_LIMIT_MINUTES * 60)
    elapsed = int(time() - started_at)
    return max(time_limit_seconds - elapsed, 0)


def _time_expired(request):
    return _remaining_seconds(request) <= 0


def _save_quiz_attempt(request, questions, answers, score, total_questions):
    quiz_attempt_id = request.session.get("quiz_attempt_id")
    if not quiz_attempt_id:
        return

    try:
        quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id, user=request.user)
    except QuizAttempt.DoesNotExist:
        return

    quiz_attempt.score = score
    quiz_attempt.total_questions = total_questions
    quiz_attempt.save(update_fields=["score", "total_questions"])

    UserAnswer.objects.filter(quiz_attempt=quiz_attempt).delete()
    answer_records = []

    for question_item in questions:
        user_answer = answers.get(str(question_item["id"]), {})
        selected_answer = user_answer.get("selected", "Not answered")
        is_correct = user_answer.get("is_correct", False)

        answer_records.append(
            UserAnswer(
                quiz_attempt=quiz_attempt,
                question_text=question_item["question"],
                user_selected_answer=selected_answer,
                correct_answer=question_item["answer"],
                is_correct=is_correct,
            )
        )

    UserAnswer.objects.bulk_create(answer_records)
