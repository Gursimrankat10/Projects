import math
import re
from collections import Counter, defaultdict

from careers import CAREERS


_TRAINING_EXAMPLES = {
    "career_fit": [
        "Which career suits my interests?",
        "How do I choose a job that fits me?",
        "What career paths should I explore?",
        "I am unsure what to do for work",
        "Is this profession right for me?",
        "Help me compare possible careers",
        "I want to change my career direction",
    ],
    "learning": [
        "How should I start learning this skill?",
        "What should I study first?",
        "I need a beginner learning plan",
        "Can you help me practice and improve?",
        "Which course or topic should I learn?",
        "How do I build experience from scratch?",
        "I want to improve my skills for this role",
    ],
    "job_search": [
        "How should I prepare for a job application?",
        "Can you help with my resume and interview?",
        "How do I get practical work experience?",
        "What should I put in a portfolio?",
        "How can I talk to someone who works in this field?",
        "I need advice on finding an internship",
        "How do I prepare for an interview?",
    ],
    "overwhelmed": [
        "I feel overwhelmed and do not know where to begin",
        "Choosing a career makes me anxious",
        "There is too much to learn and I feel stuck",
        "I am worried about making the wrong choice",
        "I feel stressed about my future",
        "I have lost motivation and need a smaller step",
        "This all feels confusing",
    ],
    "work_environment": [
        "What is the daily work like in this job?",
        "Would I work alone or with a team?",
        "What are the work hours and work setting?",
        "What is difficult about this profession?",
        "What is a typical day like?",
        "What are the good and bad sides of the role?",
        "Tell me about working conditions",
    ],
}

_STOP_WORDS = {
    "a", "an", "and", "are", "about", "be", "can", "do", "for", "from",
    "help", "how", "i", "in", "is", "it", "me", "my", "of", "on", "or",
    "should", "some", "the", "this", "to", "what", "which", "with", "would",
}


def _tokens(text):
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in _STOP_WORDS and len(token) > 1
    ]


class IntentClassifier:
    """Small, transparent multinomial Naive Bayes model trained on example prompts."""

    def __init__(self, examples):
        self.document_counts = Counter()
        self.word_counts = defaultdict(Counter)
        self.vocabulary = set()
        for label, samples in examples.items():
            for sample in samples:
                words = _tokens(sample)
                self.document_counts[label] += 1
                self.word_counts[label].update(words)
                self.vocabulary.update(words)
        self.total_documents = sum(self.document_counts.values())

    def predict(self, text):
        words = _tokens(text)
        if not words:
            return "career_fit"
        vocabulary_size = len(self.vocabulary) + 1
        scored = []
        for label, document_count in self.document_counts.items():
            total_words = sum(self.word_counts[label].values())
            score = math.log(document_count / self.total_documents)
            for word in words:
                score += math.log(
                    (self.word_counts[label][word] + 1)
                    / (total_words + vocabulary_size)
                )
            scored.append((score, label))
        return max(scored)[1]


_INTENT_MODEL = IntentClassifier(_TRAINING_EXAMPLES)


def classify_intent(message):
    return _INTENT_MODEL.predict(message)


def _closest_career(message, careers, selected_career):
    if isinstance(selected_career, str):
        selected_career = next((career for career in careers if career["id"] == selected_career), None)
    terms = set(_tokens(message))
    if terms:
        ranked = []
        for career in careers:
            description_terms = set(
                _tokens(
                    " ".join(
                        [
                            career["title"],
                            career["category"],
                            career["description"],
                            " ".join(career.get("strengths", [])),
                        ]
                    )
                )
            )
            overlap = len(terms & description_terms) / math.sqrt(
                max(1, len(terms) * len(description_terms))
            )
            ranked.append((overlap, career))
        ranked.sort(key=lambda result: result[0], reverse=True)
        if ranked and ranked[0][0] > 0:
            return ranked[0][1]
    return selected_career


def mentor_reply(message, selected_career=None):
    if isinstance(selected_career, str):
        selected_career = next((career for career in CAREERS if career["id"] == selected_career), None)
    intent = classify_intent(message)
    relevant_career = _closest_career(message, CAREERS, selected_career)
    title = relevant_career["title"] if relevant_career else None

    if intent == "overwhelmed":
        return (
            "You do not need to decide your whole future today. Pick one 10–15 minute "
            "experiment, then use what you learn—not pressure—to choose the next step. "
            "It is completely reasonable to pause or change direction."
        )
    if intent == "learning":
        first_step = relevant_career["first_step"] if relevant_career else (
            "choose one role that interests you and find a beginner lesson about it"
        )
        return (
            f"Start with one small learning goal: {first_step} "
            "Afterward, write three things you learned and one question you still have. "
            "The learning sprint on your Tasks page can help you make that concrete."
        )
    if intent == "job_search":
        return (
            f"For {title or 'a role that interests you'}, start by collecting evidence of your "
            "work: a project, a short reflection on your process, and the skills you practiced. "
            "Then draft a few questions for someone in the field. Requirements vary by employer "
            "and location, so check current local guidance before applying."
        )
    if intent == "work_environment":
        return (
            f"For {title or 'a career you are considering'}, day-to-day work can vary substantially "
            "by employer and location. Compare a few current role descriptions, noting recurring "
            "tasks, work setting, collaboration, and training requirements; then ask a practitioner "
            "what surprised them most."
        )
    if title:
        return (
            f"Your current direction is {title}. Treat that as a hypothesis, not a label: compare "
            "the daily responsibilities with what gives you energy, and try one small project before "
            "making a bigger commitment. What part of this path would you like to examine first?"
        )
    return (
        "A useful next step is to complete the assessment, then compare the suggested careers by "
        "their actual responsibilities—not just their titles. What kind of work would you like to "
        "learn more about?"
    )
