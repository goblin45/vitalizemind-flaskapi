import random

def get_keywords(emotion):
    index = random.randint(0, len(feelings_to_keywords[emotion]) - 1)
    keywords = feelings_to_keywords[emotion][index]
    keywords_arr = keywords.split()
    return keywords_arr

feelings_to_keywords = {
    'happy': [
        'cheerful songs',
    ],
    'sad': [
        'upbeat music',
        'cheerful songs',
        'positive melodies',
        'joyful tunes',        
    ],
    'anxious': [
        'calming music',
        'soothing tunes',
        'relaxing melodies',
        'peaceful sounds',
        'ambient tracks'
    ],
    'angry': [
        'heartfelt songs',
        'gentle melodies',
        'nostalgic tracks'
        'peaceful sounds',
        'ambient tracks'
    ],
    'depressed': [
        'uplifting music',
        'positive tunes',
        'calming music',
        'soothing tunes'
        
    ],
    'stressed': [
        'calming music',
        'relaxing tunes',
        'soothing melodies',
        'peaceful sounds',
        'ambient tracks'
    ]
}
