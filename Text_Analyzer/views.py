from django.shortcuts import render, redirect
from django.http import request
import regex as re

# Create your views here.
def home(request):
    if request.method == "POST":
        text = request.POST.get('textInput', '')
        stopWords = [
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
            "from", "has", "he", "in", "is", "it", "its", "of", "on", "or",
            "that", "the", "to", "was", "were", "will", "with", "you", "your"
        ]
        updated_Text = text
        word = ""
        characters=0
        para_len = 0 
        sentences = 0
        reading_time =0
        readability_text=""
        score =0 
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
            updated_Text = text.strip().upper()
        if action == 'lowercase':
            updated_Text = text.lower()
        if action == 'TitleCase':
            updated_Text = text.capitalize()
        if action == 'find':
            if find_text:
                find_matches = [match.group(0) for match in re.finditer(re.escape(find_text), text, re.IGNORECASE)]
        if action == 'replace':
            if replace_text:
                updated_Text = re.sub(re.escape(find_text), replace_text, updated_Text, flags=re.IGNORECASE)

        if action == 'find_pattern':
            if regex_pattern:
                try:
                    regex_matches = [match.group(0) for match in re.finditer(regex_pattern, text)]
                except re.error as error:
                    regex_error = str(error)
        if action == 'analyze':
            word = text.split()
            para = [p for p in text.splitlines() if p.strip()]
            para_len = len(para)
            reading_time = "{:.3f}".format(len(word)/255)
            characters = len(text)
            sentences = len([s for s in re.split(r'[.!?]+', text) if s.strip()])
            pattern = r"[\d\(\)\+\-\*\,\.\&\"\!\?]+"

            if 'remove_extra_spaces' in request.POST:
                remove_space = True
                updated_Text = re.sub(r'[ \t]+', ' ', updated_Text)

            if 'remove_punctuation' in request.POST:
                remove_punctuation = True
                updated_Text = re.sub(r"[^a-zA-Z0-9]", ' ', updated_Text)

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
                        keywords[re.sub(pattern, "", i)] = text.count(i)

        request.session['analysis_context'] = {
            "updated_Text" : updated_Text,
            "word": len(word),
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
    return render(request, 'Text_Analyzer/history.html')

def Profile(request):
    return render(request, 'Text_Analyzer/profile.html')

def login(request):
    return render(request, 'Text_Analyzer/login.html')

def logout(request):
    return render(request, 'Text_Analyzer/logout.html')

def delete(request):
    return render(request, 'Text_Analyzer/delete_user.html')