import random

def get_keywords(emotion):
    index = random.randint(0, len(feelings_to_keywords[emotion]) - 1)
    keywords = feelings_to_keywords[emotion][index]
    keywords_arr = keywords.split()
    return keywords_arr

feelings_to_keywords = {
    'happy': [
        'inspirational'
    ],
    'sad': [
        'comforting words',
        'inspirational',
        'coping strategies'
    ],
    'anxious': [
        'calming techniques',
        'stress relief methods',
        'breathing exercises',
        'coping with anxiety'
    ],
    'angry': [
        'anger management',
        'cooling down techniques',
        'resolving conflicts',
        'emotional balance',
        'healthy ways to vent'
    ],
    'depressed': [
        'coping with depression',
        'self-care practices',
        'finding purpose'

    ],
    'stressed': [
        'stress management',
        'relaxation techniques',
    
    ]
}
