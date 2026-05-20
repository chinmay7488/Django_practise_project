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
                {"name": "Recipe Meal Planner", "status": "Completed", "url": "/Recipe_Meal_Planner/"},
                {"name": "Quiz Application", "status": "Working on"},
            ],
        },
        {
            "level": "Advanced Level",
            "projects": [
                {"name": "Job Listings Board(Job Portal)", "status": "Working on"},
                {"name": "Real-time Chat Application", "status": "Working on"},
            ],
        },
    ]

    return render(request, "projects.html", {"project_groups": project_groups})
