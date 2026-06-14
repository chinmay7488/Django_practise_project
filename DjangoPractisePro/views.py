from django.shortcuts import render


def projects(request):
    project_groups = [
        {
            "level": "Beginner Level",
            "projects": [
                {"name": "To-Do list application", "status": "Completed", "url": "/TODO/"},
                {"name": "Text Analyzer", "status": "Completed", "url": "/Text_Analyzer/"},
            ],
        },
        {
            "level": "Intermediate Level",
            "projects": [
                {"name": "Recipe Meal Planner", "status": "incompleted", "url": "/Recipe_Meal_Planner/"},
                {"name": "MealMatrix", "status": "Working on", "url": "/MealMatrix/"},
                {"name": "Quiz Application", "status": "Completed", "url": "/QuizPulse/"},
            ],
        },
        {
            "level": "Websocket Level",
            "projects": [
                {"name": "Live Crypto/Stock Price Ticker Simulator", "status": "Working on", "url": "/PriceTicker/"},
                {"name": "Collaborative Real-Time Click Counter", "status": "Working on", "url": "/ClickCounter/"},
                {"name": "Real-time Chat Application", "status": "Working on", "url": "/ChatRoom/"},
            ],
        },
        {
            "level": "Advanced Level",
            "projects": [
                {"name": "Job Listings Board(Job Portal)", "status": "Working on"},
            ],
        },
    ]

    return render(request, "projects.html", {"project_groups": project_groups})
