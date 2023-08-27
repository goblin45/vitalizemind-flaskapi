import random

def get_keywords(emotion):
    index = random.randint(0, len(feelings_to_keywords[emotion]) - 1)
    keywords = feelings_to_keywords[emotion][index]
    keywords_arr = keywords.split()
    return keywords_arr

feelings_to_keywords = {
    'happy': [
        'uplifting stories',
    ],
    'sad': [
        'uplifting stories',
        'funny',
        'joyful tales',
        'inspirational',
        'happy'
    ],
    'anxious': [
        'anxiety self-help',      
        'mental health resources'
    ],
    'angry': [        
        'emotional regulation guides',      
    ],
    'depressed': [
        'motivational stories',        
        'inspirational',
        'uplifting stories',
    ],
    'stressed': [
        'stress management guides',
        'relaxation techniques books',      
    ]
}