"""
Lightweight RAG knowledge base.

For the real project: chunk documents, embed with a proper embedding model,
store vectors in the `document_chunks.embedding` pgvector column (see
/database/schema.sql), and retrieve with cosine similarity via pgvector's
`<=>` operator. This module keeps the exact same retrieve() interface but
uses an in-memory TF-IDF index over a handful of sample documents, so the
agent's RAG tool is fully functional out of the box without requiring an
embeddings API key or a running Postgres instance.

Swap `_VECTORIZER`/`_MATRIX` for a pgvector-backed lookup once real IPL
documents (rules, player profiles, venue guides, terminology) are ingested.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCUMENTS = [
    {
        "title": "IPL Playoff Format",
        "source": "internal_knowledge_base",
        "text": (
            "The IPL playoffs use a four-team format. The top two teams in the "
            "league standings play Qualifier 1, with the winner advancing "
            "directly to the final. The loser gets a second chance in "
            "Qualifier 2. Teams ranked third and fourth play the Eliminator, "
            "a knockout match. The Eliminator winner faces the Qualifier 1 "
            "loser in Qualifier 2, and that winner advances to the final."
        ),
    },
    {
        "title": "Powerplay Rules",
        "source": "internal_knowledge_base",
        "text": (
            "In IPL T20 matches, the powerplay covers the first six overs of "
            "each innings. During this period only two fielders are allowed "
            "outside the 30-yard circle, which typically encourages "
            "aggressive batting and higher scoring rates."
        ),
    },
    {
        "title": "Impact Player Rule",
        "source": "internal_knowledge_base",
        "text": (
            "The Impact Player rule lets each team make one substitution "
            "during a match from a nominated list of players, allowing a "
            "tactical swap such as bringing in an extra bowler or batter "
            "depending on how the game situation develops."
        ),
    },
    {
        "title": "Net Run Rate (NRR) Explained",
        "source": "internal_knowledge_base",
        "text": (
            "Net run rate is calculated as a team's average runs scored per "
            "over across the season minus the average runs conceded per "
            "over. It is used as a tiebreaker when two or more teams finish "
            "the league stage with equal points."
        ),
    },
    {
        "title": "Toss Impact on IPL Matches",
        "source": "internal_knowledge_base",
        "text": (
            "Historically, chasing has been slightly favored in day-night IPL "
            "matches due to dew affecting the ball late in the evening, which "
            "makes it harder for the team bowling second to grip and spin the "
            "ball, though the effect varies significantly by venue."
        ),
    },
]

_VECTORIZER = TfidfVectorizer(stop_words="english")
_MATRIX = _VECTORIZER.fit_transform([d["text"] for d in DOCUMENTS])


def retrieve(query: str, top_k: int = 3):
    query_vec = _VECTORIZER.transform([query])
    scores = cosine_similarity(query_vec, _MATRIX).flatten()
    ranked = sorted(range(len(DOCUMENTS)), key=lambda i: scores[i], reverse=True)
    results = []
    for i in ranked[:top_k]:
        if scores[i] <= 0:
            continue
        doc = DOCUMENTS[i]
        results.append({
            "title": doc["title"],
            "source": doc["source"],
            "excerpt": doc["text"],
            "relevance_score": round(float(scores[i]), 3),
        })
    return results
