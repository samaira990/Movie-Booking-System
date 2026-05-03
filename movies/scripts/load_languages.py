from movies.models import Language

def run():
    languages = [
        "Hindi", "English", "Tamil", "Telugu", "Kannada", "Malayalam",
        "Punjabi", "Marathi", "Bengali", "Gujarati",
        "Korean", "Japanese", "Spanish", "French", "Chinese"
    ]

    for lang in languages:
        Language.objects.get_or_create(name=lang)

    print("Languages added successfully!")