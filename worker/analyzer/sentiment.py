"""Sentiment analysis using Hugging Face Transformers."""

import logging
from dataclasses import dataclass
from typing import List, Literal

from transformers import pipeline

logger = logging.getLogger(__name__)

SentimentLabel = Literal["positive", "negative", "neutral"]


@dataclass
class AnalysisResult:
    """Result from sentiment analysis.

    Attributes:
        label: Sentiment classification (positive, negative, neutral).
        score: Confidence score between 0 and 1.
    """

    label: SentimentLabel
    score: float


class SentimentAnalyzer:
    """Sentiment analyzer using Hugging Face Transformers.

    Uses DistilBERT fine-tuned on SST-2 for binary sentiment classification.
    Low confidence results (<0.6) are mapped to 'neutral'.
    """

    DEFAULT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    NEUTRAL_THRESHOLD = 0.6
    MAX_TEXT_LENGTH = 512

    def __init__(self, model_name: str = DEFAULT_MODEL):
        """Initialize the sentiment analysis pipeline.

        Args:
            model_name: Hugging Face model identifier.
        """
        logger.info(f"Loading sentiment model: {model_name}")
        self._classifier = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=-1,  # Use CPU; set to 0 for GPU
        )
        logger.info("Sentiment model loaded successfully")

    def analyze(self, text: str) -> AnalysisResult:
        """Analyze sentiment of a single text.

        Args:
            text: The text to analyze.

        Returns:
            AnalysisResult with label and confidence score.
        """
        # Truncate to model's max length
        truncated = text[: self.MAX_TEXT_LENGTH]
        result = self._classifier(truncated)[0]
        return self._map_result(result)

    def analyze_batch(
        self, texts: List[str], batch_size: int = 16
    ) -> List[AnalysisResult]:
        """Analyze sentiment of multiple texts efficiently.

        Args:
            texts: List of texts to analyze.
            batch_size: Number of texts to process at once.

        Returns:
            List of AnalysisResult objects.
        """
        if not texts:
            return []

        # Truncate all texts
        truncated = [t[: self.MAX_TEXT_LENGTH] for t in texts]

        logger.info(f"Analyzing {len(truncated)} texts in batches of {batch_size}")
        results = self._classifier(truncated, batch_size=batch_size)

        return [self._map_result(r) for r in results]

    def _map_result(self, result: dict) -> AnalysisResult:
        """Map Hugging Face output to AnalysisResult.

        The DistilBERT SST-2 model returns POSITIVE/NEGATIVE.
        Low confidence results are mapped to 'neutral'.

        Args:
            result: Raw result from the classifier pipeline.

        Returns:
            Mapped AnalysisResult.
        """
        label = result["label"].lower()
        score = result["score"]

        # Map low confidence to neutral
        if score < self.NEUTRAL_THRESHOLD:
            return AnalysisResult(label="neutral", score=score)

        # Map to our label format
        if label == "positive":
            return AnalysisResult(label="positive", score=score)
        else:
            return AnalysisResult(label="negative", score=score)
