import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Download necessary NLTK data
print("Checking NLTK data...")
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
print("NLTK data ready.")

def preprocess_text(text):
    """Basic preprocessing: lowercase and stopword removal for TF-IDF."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return " ".join(filtered_words)

def generate_summary(text, num_sentences=5):
    """Generates an extractive summary using TF-IDF."""
    if not text.strip():
        return ""

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    # Preprocess each sentence
    preprocessed_sentences = [preprocess_text(s) for s in sentences]

    # Filter out empty preprocessed sentences to avoid TF-IDF errors
    valid_sentences = []
    valid_preprocessed = []
    for i, s in enumerate(preprocessed_sentences):
        if s.strip():
            valid_sentences.append(sentences[i])
            valid_preprocessed.append(s)

    if not valid_preprocessed:
        return sentences[0] if sentences else ""

    try:
        # Calculate TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(valid_preprocessed)

        # Calculate sentence scores
        sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

        # Rank sentences
        num_to_pick = min(num_sentences, len(valid_sentences))
        top_sentence_indices = sentence_scores.argsort()[-num_to_pick:][::-1]
        top_sentence_indices.sort()

        summary = " ".join([valid_sentences[i] for i in top_sentence_indices])
        return summary
    except Exception as e:
        print(f"Summarizer Warning: {e}")
        return " ".join(sentences[:num_sentences]) # Fallback to first few sentences
