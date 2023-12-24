from abc import ABC, abstractmethod
import logging
from transformers import pipeline
from thefuzz import fuzz, process


class TextClassifier(ABC):
    """
    Abstract class for text classifier
    """

    @abstractmethod
    def predict(self, text, labels):
        """
        Given a text and a list of labels, predict the label for the text
        """
        pass

    @abstractmethod
    def predict_batch(self, texts, labels):
        """
        Given a list of texts and a list of labels, predict the labels for the texts
        """
        pass


class SimpleClassifier(TextClassifier):
    """
    This classifier will be used to classify the text using NLP techniques.
    It uses a pre-trained model from huggingface.
    """

    def __init__(self, model="facebook/bart-large-mnli", threshold=0.9) -> None:
        self.model = model
        self.pipe = None  # only initialize the pipeline when needed
        self.threshold = threshold

    def predict(self, text, labels):
        logging.info("Simple Predicting category for %s", text)
        if not self.pipe:
            self.pipe = pipeline("zero-shot-classification", model=self.model)
        logging.debug("Simple Labels: %s", labels)
        result = self.pipe(text, labels)
        if result["scores"][0] < self.threshold:
            logging.debug(
                "Label %s score %s is below threshold %s",
                result["labels"][0],
                result["scores"][0],
                self.threshold,
            )
            return None
        predicted_label = result["labels"][0]
        logging.info("Simple Predicted label: %s", predicted_label)
        return predicted_label

    def predict_batch(self, texts, labels):
        logging.info("Simple Predicting categories for %s", texts)
        if not self.pipe:
            self.pipe = pipeline("zero-shot-classification", model=self.model)
        result = self.pipe(texts, labels)
        logging.debug("Simple Result: %s", result)
        predicted_labels = [r["labels"][0] for r in result]
        logging.info("Simple Predicted labels: %s", predicted_labels)
        return predicted_labels


def fuzzy_search(text, labels, threshold=85, scorer=fuzz.token_set_ratio):
    """
    Given a text and a list of labels, find the label that best matches the text
    """
    if not labels:
        logging.warning("No labels provided for %s, returning None", text)
        return None

    logging.info("Fuzzy Predicting label for %s", text)
    logging.debug("Fuzzy Labels: %s", labels)
    best_label, best_score = process.extractOne(text, labels, scorer=scorer)
    logging.debug("Fuzzy Best label: %s. score %s", best_label, best_score)
    if best_score < threshold:
        logging.warning("Fuzzy score is below threshold: %s", best_score)
        return None
    logging.info("Fuzzy Predicted label: %s", best_label)
    return best_label
