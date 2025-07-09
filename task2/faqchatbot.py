from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_faqs():
    """
    Returns a list of (question, answer) tuples.
    You can replace or extend these with your own FAQs.
    """
    return [
        ("What is your return policy?",
         "You can return any item within 30 days of purchase for a full refund."),
        ("How do I track my order?",
         "Once your order ships, we will send you an email with a tracking number."),
        ("Do you ship internationally?",
         "Yes—we ship to most countries worldwide. Shipping rates vary by location."),
        ("How can I contact customer support?",
         "You can reach us at support@example.com or call 1‑800‑123‑4567."),
        ("What payment methods do you accept?",
         "We accept Visa, MasterCard, American Express, and PayPal."),
    ]

def build_vectorizer(questions):
    """
    Fit a TF‑IDF vectorizer on the FAQ questions.
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words="english",
        ngram_range=(1,2),
    )
    tfidf_matrix = vectorizer.fit_transform(questions)
    return vectorizer, tfidf_matrix

def find_best_answer(user_q, faqs, vectorizer, faq_tfidf):
    """
    Given a user question, return the FAQ answer with the highest cosine similarity.
    """
    user_vec = vectorizer.transform([user_q])
    sims = cosine_similarity(user_vec, faq_tfidf)[0]
    best_idx = sims.argmax()
    best_score = sims[best_idx]
    if best_score < 0.2:
        return None, best_score
    return faqs[best_idx][1], best_score

def chat_loop():
    faqs = load_faqs()
    questions = [q for q, a in faqs]
    vectorizer, faq_tfidf = build_vectorizer(questions)

    print("🤖 FAQ Chatbot is ready! (type 'exit' or 'quit' to stop)\n")
    while True:
        user_q = input("You: ").strip()
        if user_q.lower() in {"exit", "quit"}:
            print("🤖 Goodbye!")
            break

        answer, score = find_best_answer(user_q, faqs, vectorizer, faq_tfidf)
        if answer:
            print(f"🤖 {answer}  (confidence: {score:.2f})\n")
        else:
            print("🤖 Sorry, I don't know the answer to that. Can you rephrase?\n")

if __name__ == "__main__":
    chat_loop()