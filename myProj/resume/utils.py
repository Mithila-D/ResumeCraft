


from django.shortcuts import render
from django.http import HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

job_keywords = {
    "Data Scientist": {
        "technical_skills": [
            "data analysis", "machine learning", "statistics", "big data", "predictive modeling",
            "data visualization", "deep learning", "NLP", "data wrangling", "data mining"
        ],
        "tools_and_libraries": [
            "Python", "R", "SQL", "TensorFlow", "Keras", "scikit-learn", "Apache Spark",
            "Hadoop", "Pandas", "NumPy", "Jupyter Notebook", "Tableau", "Power BI", "D3.js"
        ],
        "soft_skills": [
            "critical thinking", "problem-solving", "attention to detail", "communication",
            "collaboration", "adaptability", "analytical mindset", "continuous learning"
        ],
        "achievements": [
            "published research", "data competition participation", "ML model deployment",
            "patent contributions", "conference presentations", "top Kaggle scores"
        ]
    },
    "Software Developer": {
        "technical_skills": [
            "coding", "algorithms", "debugging", "object-oriented programming", "problem-solving",
            "testing", "optimization", "scalability", "performance tuning"
        ],
        "tools_and_libraries": [
            "JavaScript", "Python", "C++", "Java", "SQL", "Git", "Docker", "Kubernetes",
            "Jenkins", "REST APIs", "Spring", "Django", "Node.js", "React", "Angular", "AWS"
        ],
        "soft_skills": [
            "teamwork", "time management", "communication", "attention to detail", "creativity",
            "adaptability", "collaborative mindset", "continuous improvement"
        ],
        "achievements": [
            "open-source contributions", "hackathon participation", "certifications",
            "side projects", "personal portfolio", "technical leadership"
        ]
    },
    "Business Analyst": {
        "technical_skills": [
            "analytics", "data visualization", "stakeholder engagement", "problem-solving",
            "requirement analysis", "project management", "reporting", "business case development"
        ],
        "tools_and_libraries": [
            "Excel", "Power BI", "SQL", "Tableau", "Jira", "Confluence", "Microsoft Project",
            "Visio", "Google Analytics", "SPSS", "SAS", "Qlik"
        ],
        "soft_skills": [
            "analytical thinking", "communication", "stakeholder management", "adaptability",
            "strategic thinking", "negotiation", "presentation skills"
        ],
        "achievements": [
            "project completions", "certifications in business analysis", "recognition awards",
            "process improvements", "successful project delivery"
        ]
    },
    "Front-End Developer": {
        "technical_skills": [
            "HTML", "CSS", "JavaScript", "user interface design", "responsive design", "UX/UI",
            "SEO", "web accessibility", "cross-browser compatibility", "user-centric design"
        ],
        "tools_and_libraries": [
            "React", "Vue.js", "Angular", "Bootstrap", "Sass", "Figma", "Sketch",
            "Adobe XD", "Webpack", "Babel", "Git", "Photoshop", "Illustrator"
        ],
        "soft_skills": [
            "creativity", "attention to detail", "communication", "adaptability", "problem-solving",
            "time management"
        ],
        "achievements": [
            "portfolio of design projects", "successful website launches", "UI/UX certifications",
            "contributions to design systems", "recognition for design aesthetics"
        ]
    },
    "Full-Stack Developer": {
        "technical_skills": [
            "full-stack development", "RESTful APIs", "database management", "cloud computing",
            "server-side programming", "web security", "scalability"
        ],
        "tools_and_libraries": [
            "JavaScript", "Node.js", "React", "Express", "MongoDB", "PostgreSQL", "MySQL",
            "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "Git", "GraphQL", "TypeScript"
        ],
        "soft_skills": [
            "problem-solving", "adaptability", "collaboration", "communication", "time management",
            "attention to detail"
        ],
        "achievements": [
            "successful app deployments", "cross-functional project work", "API integration projects",
            "certifications in full-stack development", "open-source contributions"
        ]
    }
}

experience_keywords = {
    "fresher": [
        "internships", "certifications", "volunteering", "academic projects", "team player",
        "eager to learn", "entry-level", "basic knowledge", "enthusiasm", "foundation skills"
    ],
    "experienced": [
        "leadership", "project management", "mentorship", "senior roles", "specialization",
        "expertise", "results-oriented", "strategy", "advanced skills", "problem-solving at scale"
    ]
}


from django.shortcuts import render
from .forms import ResumeForm
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from textblob import TextBlob

ignore_terms = [
    'predictive', 'mindset', 'data', 'machine', 'learning', 'big', 'data', 
    'visualization', 'deep', 'NLP', 'wrangling', 'mining', 'Python', 'R', 
    'SQL', 'TensorFlow', 'Keras', 'scikit-learn', 'Apache', 'Spark', 'Hadoop', 
    'Pandas', 'NumPy', 'Jupyter', 'Tableau', 'Power', 'BI', 'D3.js'
]

def check_spelling(text):
    # Initialize TextBlob object
    blob = TextBlob(text)
    
    # List to hold spelling errors
    errors = []

    # Split the text into words
    words = text.split()

    # Check each word for spelling errors, ignoring known technical terms
    for word in words:
        if word.lower() not in ignore_terms:  
            corrected_word = TextBlob(word).correct()
            corrected_word_str = str(corrected_word)   
            if corrected_word_str != word:  # If the word was corrected, it's considered an error
                errors.append((word, corrected_word_str))
 
    corrected_text = ' '.join([str(TextBlob(word).correct()) if word.lower() not in ignore_terms else word for word in words])
    return corrected_text, errors


















































from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
 
nltk.download('punkt')
nltk.download('stopwords')
 
def preprocess_text(text):
    if not text:  # Handle empty or None inputs
        return []
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower()) 
   
    return [word for word in tokens if word.isalnum() and len(word) > 1 and word not in stop_words]
 
def match_section(user_section, required_keywords, section_name):
    required_text = ' '.join(preprocess_text(' '.join([str(kw).lower() for kw in required_keywords])))
    user_text = ' '.join(preprocess_text(' '.join([str(item).lower() for item in user_section])))
 
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([required_text, user_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2]).flatten()[0]

    print(f"Matching {section_name} - Similarity: {similarity}")   
    print(f"Required Text: {required_text}")
    print(f"User Text: {user_text}")

    threshold = 0.3   
    if similarity >= threshold:
        return None   
    else:
        user_set = set(user_section)
        missing_keywords = [kw for kw in required_keywords if kw not in user_set]
        print(f"Missing {section_name}: {missing_keywords}")   
        return missing_keywords
 
def clean_input(input_str):
    if not input_str:  
        return []
    return [item.strip() for item in input_str.split(',') if item.strip()]
 
def match_keywords(user_data, job_role, experience_level):
    user_data["technical_skills"] = clean_input(user_data.get("technical_skills", ""))
    user_data["tools_and_libraries"] = clean_input(user_data.get("tools_and_libraries", ""))
    user_data["soft_skills"] = clean_input(user_data.get("soft_skills", ""))
    user_data["achievements"] = clean_input(user_data.get("achievements", ""))

    feedback = {}
 
    technical_skills_feedback = match_section(
        user_data["technical_skills"],
        job_keywords[job_role]["technical_skills"],
        "technical skills"
    )
    if technical_skills_feedback:
        feedback["technical_skills"] = technical_skills_feedback

    tools_feedback = match_section(
        user_data["tools_and_libraries"],
        job_keywords[job_role]["tools_and_libraries"],
        "tools and libraries"
    )
    if tools_feedback:
        feedback["tools_and_libraries"] = tools_feedback

    soft_skills_feedback = match_section(
        user_data["soft_skills"],
        job_keywords[job_role]["soft_skills"],
        "soft skills"
    )
    if soft_skills_feedback:
        feedback["soft_skills"] = soft_skills_feedback

    achievements_feedback = match_section(
        user_data["achievements"],
        experience_keywords[experience_level],
        "achievements"
    )
    if achievements_feedback:
        feedback["achievements"] = achievements_feedback

    return feedback
