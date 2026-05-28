from random import shuffle
from time import time

from django.shortcuts import redirect, render


PASS_PERCENTAGE = 70
TIME_LIMIT_MINUTES = 5

CATEGORIES = {
    "18": "Science: Computers",
    "9": "General Knowledge",
    "17": "Science & Nature",
}

QUESTION_BANK = [
    {
        "id": 1,
        "category": "18",
        "difficulty": "easy",
        "type": "multiple",
        "question": "What does CPU stand for?",
        "choices": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing User"],
        "answer": "Central Processing Unit",
    },
    {
        "id": 2,
        "category": "18",
        "difficulty": "medium",
        "type": "multiple",
        "question": "Which data structure works on a First In, First Out principle?",
        "choices": ["Queue", "Stack", "Tree", "Graph"],
        "answer": "Queue",
    },
    {
        "id": 3,
        "category": "18",
        "difficulty": "hard",
        "type": "multiple",
        "question": "Which normal form removes transitive dependencies in relational databases?",
        "choices": ["Third Normal Form", "First Normal Form", "Second Normal Form", "Boyce-Codd Normal Form"],
        "answer": "Third Normal Form",
    },
    {
        "id": 4,
        "category": "18",
        "difficulty": "easy",
        "type": "boolean",
        "question": "HTML is a programming language.",
        "choices": ["True", "False"],
        "answer": "False",
    },
    {
        "id": 5,
        "category": "9",
        "difficulty": "easy",
        "type": "multiple",
        "question": "How many days are there in a leap year?",
        "choices": ["366", "365", "364", "367"],
        "answer": "366",
    },
    {
        "id": 6,
        "category": "9",
        "difficulty": "medium",
        "type": "boolean",
        "question": "The Great Wall of China is visible from the Moon with the naked eye.",
        "choices": ["True", "False"],
        "answer": "False",
    },
    {
        "id": 7,
        "category": "17",
        "difficulty": "easy",
        "type": "multiple",
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Mars", "Venus", "Jupiter", "Mercury"],
        "answer": "Mars",
    },
    {
        "id": 8,
        "category": "17",
        "difficulty": "medium",
        "type": "multiple",
        "question": "What is the chemical symbol for gold?",
        "choices": ["Au", "Ag", "Gd", "Go"],
        "answer": "Au",
    },
    {
        "id": 9,
        "category": "17",
        "difficulty": "hard",
        "type": "boolean",
        "question": "Sound travels faster in water than in air.",
        "choices": ["True", "False"],
        "answer": "True",
    },
    {
        "id": 10,
        "category": "9",
        "difficulty": "hard",
        "type": "multiple",
        "question": "Which ancient wonder was located in Alexandria?",
        "choices": ["The Lighthouse", "The Hanging Gardens", "The Colossus", "The Mausoleum"],
        "answer": "The Lighthouse",
    },
]


def home(request):
    return render(
        request,
        "QuizPulse/home.html",
        {
            "categories": CATEGORIES,
            "difficulties": ["easy", "medium", "hard"],
            "question_types": [("multiple", "Multiple Choice"), ("boolean", "True / False")],
        },
    )


def start_quiz(request):
    if request.method != "POST":
        return redirect("QuizPulse:home")

    amount = int(request.POST.get("amount", 5))
    category = request.POST.get("category")
    difficulty = request.POST.get("difficulty")
    question_type = request.POST.get("question_type")

    questions = [
        question
        for question in QUESTION_BANK
        if question["category"] == category
        and question["difficulty"] == difficulty
        and question["type"] == question_type
    ]

    if len(questions) < amount:
        questions = [
            question
            for question in QUESTION_BANK
            if question["category"] == category and question["type"] == question_type
        ]

    if len(questions) < amount:
        questions = QUESTION_BANK.copy()

    shuffle(questions)
    selected_questions = questions[:amount]

    request.session["quiz_questions"] = selected_questions
    request.session["current_question_index"] = 0
    request.session["answers"] = {}
    request.session["score"] = 0
    request.session["started_at"] = time()
    request.session["time_limit_seconds"] = TIME_LIMIT_MINUTES * 60
    request.session.modified = True

    return redirect("QuizPulse:question")


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


def results(request):
    questions = request.session.get("quiz_questions", [])
    answers = request.session.get("answers", {})
    score = sum(1 for answer in answers.values() if answer["is_correct"])
    total_questions = len(questions)
    percentage = round((score / total_questions) * 100) if total_questions else 0
    passed = percentage >= PASS_PERCENTAGE
    timed_out = _time_expired(request)

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


def review(request):
    questions = request.session.get("quiz_questions", [])
    answers = request.session.get("answers", {})
    review_items = []

    for question_item in questions:
        user_answer = answers.get(str(question_item["id"]), {})
        review_items.append(
            {
                "question": question_item,
                "selected": user_answer.get("selected", "Not answered"),
                "is_correct": user_answer.get("is_correct", False),
            }
        )

    return render(request, "QuizPulse/review.html", {"review_items": review_items})


def restart(request):
    for key in [
        "quiz_questions",
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
