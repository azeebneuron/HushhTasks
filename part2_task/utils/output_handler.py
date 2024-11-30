# output_handler.py
import os
import json
from datetime import datetime
import pandas as pd

class OutputHandler:
    def __init__(self):
        """Initialize output directory structure"""
        # Create main output directories
        self.output_dir = "output"
        self.dirs = {
            'raw': f"{self.output_dir}/raw_results",
            'comparisons': f"{self.output_dir}/comparisons",
            'reports': f"{self.output_dir}/reports",
            'visualizations': f"{self.output_dir}/visualizations"
        }
        
        for directory in self.dirs.values():
            os.makedirs(directory, exist_ok=True)

    def save_result(self, result, model_name, text_type):
        """Save individual model results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{model_name}_{text_type}_{timestamp}.json"
        filepath = os.path.join(self.dirs['raw'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        return filepath

    def save_comparison(self, comparison, text_type):
        """Save comparison results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"comparison_{text_type}_{timestamp}.json"
        filepath = os.path.join(self.dirs['comparisons'], filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, default=str)
        
        return filepath

    def generate_report(self, all_results):
        """Generate and save summary report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create summary metrics
        summary = {
            'timestamp': timestamp,
            'total_processed': len(all_results),
            'model_comparison': {
                'sentiment_agreement_rate': sum(r['metrics']['sentiment_match'] for r in all_results) / len(all_results),
                'average_topic_overlap': sum(r['metrics']['topic_overlap'] for r in all_results) / len(all_results),
                'average_confidence_difference': sum(r['metrics']['confidence_difference'] for r in all_results) / len(all_results)
            }
        }
        
        # Save summary report as JSON
        report_path = os.path.join(self.dirs['reports'], f'summary_report_{timestamp}.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Create CSV report for easy viewing
        csv_data = []
        for result in all_results:
            csv_data.append({
                'text_type': result.get('text_type', 'Unknown'),
                'sentiment_match': result['metrics']['sentiment_match'],
                'topic_overlap': result['metrics']['topic_overlap'],
                'confidence_difference': result['metrics']['confidence_difference']
            })
        
        df = pd.DataFrame(csv_data)
        csv_path = os.path.join(self.dirs['reports'], f'detailed_report_{timestamp}.csv')
        df.to_csv(csv_path, index=False)
        
        return report_path, csv_path