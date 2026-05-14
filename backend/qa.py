from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize

def answer_question(question, document_text, summary=""):
    """Finds the most relevant sentence in the document for the given question."""
    if not document_text.strip():
        return "I don't have any text to answer from."

    # Handle very generic questions by returning the summary
    generic_keywords = ['about', 'summarize', 'summary', 'overview', 'content', 'pdf', 'paper']
    question_lower = question.lower()
    if any(word in question_lower for word in generic_keywords) and len(question.split()) < 5:
        if summary:
            return f"Here is a summary of the paper: {summary}"

    sentences = sent_tokenize(document_text)
    if not sentences:
        return "The document seems to be empty."

    try:
        # Use n-grams (1,2) for better context matching
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        
        # Combine question and sentences
        tfidf_matrix = vectorizer.fit_transform([question] + sentences)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Find the index of the most similar sentence
        best_match_idx = similarities.argmax()
        score = similarities[0][best_match_idx]
        
        print(f"Q&A Debug - Best Score: {score:.4f}")
        
        # Lower threshold and fallback to summary if score is too low
        if score < 0.05:
            if summary:
                return f"I couldn't find a specific section, but here is what the paper is generally about: {summary}"
            return "I'm sorry, I couldn't find a relevant section in the document to answer that."
            
        # --- NEW: Context Window Logic ---
        # Get the matching sentence and its neighbors for more complete answers
        start_idx = max(0, best_match_idx - 1)
        end_idx = min(len(sentences), best_match_idx + 2)
        
        context_sentences = sentences[start_idx:end_idx]
        answer = " ".join(context_sentences)
        
        return answer
    except Exception as e:
        print(f"QA Error: {e}")
        return f"I encountered an error, but here is the summary: {summary}" if summary else "Error processing question."
