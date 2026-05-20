from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
import regex as re
from .models import AnalyzeSave

# Create your views here.
def home(request):
    if request.method == "POST":
        global characters
        global  para_len 
        global  sentences
        global  reading_time
        global score
        global  word_count
        global original_text 
        global updated_text
        original_text = request.POST.get('textInput', '')
        stopWords = [
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
            "from", "has", "he", "in", "is", "it", "its", "of", "on", "or",
            "that", "the", "to", "was", "were", "will", "with", "you", "your"
        ]
        updated_text = original_text
        word = ""
        readability_text=""
        keywords={}
        remove_space = True
        remove_punctuation = False
        find_text = request.POST.get('find_text', '').strip()
        replace_text = request.POST.get('replace_text', '').strip()
        regex_pattern = request.POST.get('regex_pattern', '').strip()
        find_matches = []
        regex_matches = []
        regex_error = ""

        action = request.POST.get('action')
        if action == 'uppercase':
            updated_text = original_text.strip().upper()
        if action == 'lowercase':
            updated_text = original_text.lower()
        if action == 'TitleCase':
            updated_text = original_text.capitalize()
        if action == 'find':
            if find_text:
                find_matches = [match.group(0) for match in re.finditer(re.escape(find_text), original_text, re.IGNORECASE)]
        if action == 'replace':
            if replace_text:
                updated_text = re.sub(re.escape(find_text), replace_text, updated_text, flags=re.IGNORECASE)

        if action == 'find_pattern':
            if regex_pattern:
                try:
                    regex_matches = [match.group(0) for match in re.finditer(regex_pattern, original_text)]
                except re.error as error:
                    regex_error = str(error)
        if action == 'analyze':
            word = original_text.split()
            word_count = len(word)
            para = [p for p in original_text.splitlines() if p.strip()]
            para_len = len(para)
            reading_time = "{:.3f}".format(word_count/255)
            characters = len(original_text)
            sentences = len([s for s in re.split(r'[.!?]+', original_text) if s.strip()])
            pattern = r"[\d\(\)\+\-\*\,\.\&\"\!\?]+"

            if 'remove_extra_spaces' in request.POST:
                remove_space = True
                updated_text = re.sub(r'[ \t]+', ' ', updated_text)

            if 'remove_punctuation' in request.POST:
                remove_punctuation = True
                updated_text = re.sub(r"[^a-zA-Z0-9]", ' ', updated_text)

            if word:
                total_syllables = sum(count_syllables(w) for w in word)
                safe_sentence_count = max(sentences, 1)
                score = 206.835 - 1.015 * (len(word)/safe_sentence_count) - 84.6 * (total_syllables/len(word))
                if (score >= 90):
                    readability_text =  "Very easy to read."
                elif (score >= 70) :
                    readability_text =  "Easy to read."
                elif (score >= 50) :
                    readability_text =  "Fairly readable."
                elif (score >= 30) :
                    readability_text =  "Difficult to read."
                else:
                    readability_text =  "Very difficult to read."

            
                for i in word:
                    if i.lower() not in stopWords and not re.match(pattern,i):
                        keywords[re.sub(pattern, "", i)] = original_text.count(i)

        request.session['analysis_context'] = {
            "updated_Text" : updated_text,
            "word": word_count,
            'character':characters,
            'paragraphs': para_len,
            "sentences" : sentences,
            'reading_Time' : reading_time,
            "readability_text":readability_text,
            'keyword_items': list(keywords.items()),
            'remove_punctuation': remove_punctuation,
            'remove_extra_spaces': remove_space,
            'find_text': find_text,
            'replace_text': replace_text,
            'regex_pattern': regex_pattern,
            'find_matches': find_matches,
            'find_count': len(find_matches),
            'regex_matches': regex_matches,
            'regex_count': len(regex_matches),
            'regex_error': regex_error,
        }
        return redirect('TAnalyzer:home')

    context = request.session.pop('analysis_context', {})
    return render(request, 'Text_Analyzer/index.html', context=context)

def feature(request):
    return render(request, 'Text_Analyzer/features.html')

def count_syllables(word):
    word = word.lower().strip()
    if not word:
        return 0
    
    vowels = "aeiouy"
    count = 0
    
    # Rule 1: Count every vowel in the word
    if word[0] in vowels:
        count += 1
        
    for i in range(1, len(word)):
        # Rule 2: Count a vowel only if the previous character was NOT a vowel
        # This handles "vowel teams" (diphthongs) like 'oo', 'ea', 'ai'
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
            
    # Rule 3: Subtract 1 for a silent 'e' at the end
    if word.endswith("e"):
        count -= 1
        
    # Rule 4: Every word must have at least one syllable
    if count <= 0:
        count = 1
        
    return count

def History(request):
    if request.user.is_authenticated:
        data = AnalyzeSave.objects.filter(Person = request.user)

        return render(request, 'Text_Analyzer/history.html', context={
            "User_history" : data
        })
    return render(request, 'Text_Analyzer/history.html')

def Profile(request):
    data = AnalyzeSave.objects.filter(Person = request.user)
    print()
    context = {
        'current_user': request.user,
        "User_history" : data,
        "Total_words" : data.aggregate(Sum('words_count'))['words_count__sum'],
        "Saved_Analyzes" : data.count(),
    }
    
    return render(request, 'Text_Analyzer/profile.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember') == "on"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if remember_me:
                request.session.set_expiry(1209600) 
            else:
                request.session.set_expiry(0)
            return redirect('TAnalyzer:home')
        else:
            error_messages =  "Invalid username or password."

        return render(request, 'Text_Analyzer/login.html', {"error_messages": error_messages})

    return render(request, 'Text_Analyzer/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'Text_Analyzer/signup.html', {"error_messages": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'Text_Analyzer/signup.html', {"error_messages": "Username already taken!"})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('TAnalyzer:login')

    return render(request, 'Text_Analyzer/signup.html')

def logout_page(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('TAnalyzer:home')

    return render(request, 'Text_Analyzer/logout.html')

def delete(request):
    return render(request, 'Text_Analyzer/delete_user.html')

def Save_Analyze(request):
    if request.user.is_authenticated:
        
        AnalyzeSave.objects.create(
            Person = request.user,
            Title = 'Title',
            words_count = word_count,
            orginal_text = original_text,
            updated_text = updated_text,
            sentence_count = sentences,
            character_count = characters,
            paragraph_count = para_len,
            readablity_score = score
        )

        return redirect('TAnalyzer:home')