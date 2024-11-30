# utils/comparison.py
from typing import Dict, List, Tuple, Optional
from models.pydantic_models import ProcessedData
from datetime import datetime
import json
import os
from collections import Counter

class ModelComparison:
    def __init__(self):
        """Initialize comparison utilities"""
        os.makedirs('output/comparisons', exist_ok=True)
        os.makedirs('output/reports', exist_ok=True)

    def calculate_topic_overlap(self, topics1: List[str], topics2: List[str]) -> float:
        """
        Calculate Jaccard similarity between topic lists
        """
        # Convert topics to lowercase for better comparison
        set1 = set(topic.lower() for topic in topics1)
        set2 = set(topic.lower() for topic in topics2)
        
        if not set1 and not set2:
            return 1.0
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0

    def calculate_summary_similarity(self, summary1: str, summary2: str) -> float:
        """
        Calculate similarity between summaries using word overlap
        """
        # Convert to lowercase and split into words
        words1 = set(summary1.lower().split())
        words2 = set(summary2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0

    # utils/comparison.py
    def compare_responses(self, gemini_response, llama_response):
        """Compare responses from both models"""
        gemini_data = gemini_response.model_dump()  # Updated from dict()
        llama_data = llama_response.model_dump()    # Updated from dict()
        
        comparison = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {
                'sentiment_match': gemini_data['sentiment'] == llama_data['sentiment'],
                'topic_overlap': self.calculate_topic_overlap(
                    gemini_data['key_topics'], 
                    llama_data['key_topics']
                ),
                'confidence_difference': abs(
                    gemini_data['confidence_score'] - llama_data['confidence_score']
                ),
                'summary_similarity': self.calculate_summary_similarity(
                    gemini_data['summary'],
                    llama_data['summary']
                )
            },
            'responses': {
                'gemini': gemini_data,
                'llama': llama_data
            }
        }
        
        return comparison

    def save_comparison(self, comparison: Dict, filename: Optional[str] = None) -> str:
        """
        Save comparison results to file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'comparison_{timestamp}.json'
        
        filepath = os.path.join('output/comparisons', filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(comparison, f, indent=2, ensure_ascii=False)
            return filepath
        except Exception as e:
            print(f"Error saving comparison: {str(e)}")
            return ""

    def load_comparisons(self, directory: str = 'output/comparisons') -> List[Dict]:
        """
        Load all comparison results from directory
        """
        comparisons = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        comparison = json.load(f)
                        comparisons.append(comparison)
        except Exception as e:
            print(f"Error loading comparisons: {str(e)}")
        
        return comparisons

    def generate_report(self, comparisons: List[Dict]) -> Dict:
        """
        Generate statistical report from multiple comparisons
        """
        if not comparisons:
            return {"error": "No comparisons available"}

        # Collect metrics
        sentiment_matches = []
        topic_overlaps = []
        summary_similarities = []
        confidence_diffs = []
        gemini_topics = []
        llama_topics = []

        for comp in comparisons:
            metrics = comp['metrics']
            details = comp['details']
            
            sentiment_matches.append(metrics['sentiment_match'])
            topic_overlaps.append(metrics['topic_overlap'])
            summary_similarities.append(metrics.get('summary_similarity', 0))
            confidence_diffs.append(metrics['confidence_difference'])
            
            gemini_topics.extend(details['gemini']['topics'])
            llama_topics.extend(details['llama']['topics'])

        # Calculate statistics
        def calculate_stats(values: List[float]) -> Dict:
            sorted_values = sorted(values)
            return {
                'mean': sum(values) / len(values) if values else 0,
                'median': sorted_values[len(values)//2] if values else 0,
                'min': min(values) if values else 0,
                'max': max(values) if values else 0
            }

        # Generate report
        report = {
            'summary': {
                'total_comparisons': len(comparisons),
                'sentiment_agreement_rate': sum(sentiment_matches) / len(sentiment_matches),
                'average_topic_overlap': sum(topic_overlaps) / len(topic_overlaps),
                'average_summary_similarity': sum(summary_similarities) / len(summary_similarities),
                'average_confidence_diff': sum(confidence_diffs) / len(confidence_diffs)
            },
            'detailed_metrics': {
                'topic_overlap_stats': calculate_stats(topic_overlaps),
                'summary_similarity_stats': calculate_stats(summary_similarities),
                'confidence_diff_stats': calculate_stats(confidence_diffs)
            },
            'topic_analysis': {
                'gemini_most_common': Counter(gemini_topics).most_common(5),
                'llama_most_common': Counter(llama_topics).most_common(5)
            },
            'timestamp': datetime.now().isoformat()
        }

        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join('output/reports', f'report_{timestamp}.json')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report