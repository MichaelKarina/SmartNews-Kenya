KEYWORDS = {
    "politics": ["ruto", "uhuru", "parliament", "azimio", "elections"],
    "football": ["manchester", "arsenal", "chelsea", "kpl", "afcon", "goal"],
    "religion": ["pastor", "church", "revival", "gospel", "prophecy"],
    "jobs": ["job", "vacancy", "recruitment", "internship", "career"],
    "trending": ["trending", "viral", "breaking"]
}

def categorize_article(title):
    title_lower = title.lower()
    for category, keywords in KEYWORDS.items():
        if any(word in title_lower for word in keywords):
            return category
    return "general"
