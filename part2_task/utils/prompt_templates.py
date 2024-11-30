# utils/prompt_templates.py

ANALYSIS_PROMPT = """
Please analyze the following text and provide a structured response. Focus on extracting key information and maintaining consistency in the analysis.

Text to analyze:
{text}

Please provide your analysis in the following JSON format:
{
    "sentiment": "one of [positive, negative, neutral]",
    "key_topics": ["list of main topics, maximum 10"],
    "summary": "2-3 sentence summary of the content",
    "confidence_score": "float between 0 and 1"
}

Requirements:
1. Sentiment must be exactly one of: positive, negative, or neutral
2. Include 1-10 key topics as a list
3. Summary should be concise but informative
4. Confidence score should reflect your certainty in the analysis

Respond ONLY with the JSON object, no additional text or explanations.
"""

# Additional templates can be added here for different analysis types
SENTIMENT_ONLY_PROMPT = """
Analyze the sentiment of the following text and respond with a JSON object:

Text: {text}

Response format:
{
    "sentiment": "one of [positive, negative, neutral]",
    "confidence_score": "float between 0 and 1"
}
"""

TOPIC_EXTRACTION_PROMPT = """
Extract the main topics from the following text and respond with a JSON object:

Text: {text}

Response format:
{
    "key_topics": ["list of main topics, maximum 10"],
    "confidence_score": "float between 0 and 1"
}
"""