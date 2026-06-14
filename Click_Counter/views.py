from django.shortcuts import render

# Create your views here.
def counter(request):
    return render(request, 'Click_Counter/counter.html')