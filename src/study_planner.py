"""
Study Plan & Schedule Generator
Creates realistic academic planning based on subject, hours, and study scenario
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

class StudyPlanner:
    def __init__(self):
        """Initialize the study planner"""
        self.subject_complexity = {
            'Mathematics': {'reading': 0.3, 'practice': 0.5, 'revision': 0.2},
            'Physics': {'reading': 0.35, 'practice': 0.45, 'revision': 0.2},
            'Chemistry': {'reading': 0.4, 'practice': 0.4, 'revision': 0.2},
            'Biology': {'reading': 0.5, 'practice': 0.3, 'revision': 0.2},
            'Computer Science': {'reading': 0.25, 'practice': 0.6, 'revision': 0.15},
            'English': {'reading': 0.6, 'practice': 0.25, 'revision': 0.15},
            'History': {'reading': 0.7, 'practice': 0.15, 'revision': 0.15}
        }
        
        self.scenario_adjustments = {
            'exam_prep': {
                'reading': 0.8,
                'practice': 1.2,
                'revision': 1.5,
                'intensity': 'high'
            },
            'homework': {
                'reading': 1.0,
                'practice': 1.3,
                'revision': 0.7,
                'intensity': 'medium'
            },
            'general_study': {
                'reading': 1.1,
                'practice': 1.0,
                'revision': 0.9,
                'intensity': 'low'
            },
            'project_work': {
                'reading': 0.7,
                'practice': 1.5,
                'revision': 0.8,
                'intensity': 'medium'
            }
        }
        
    def calculate_time_distribution(self, subject, total_hours, scenario='general_study'):
        """Calculate optimal time distribution for reading, practice, and revision"""
        # Get base distribution for subject
        if subject in self.subject_complexity:
            base_dist = self.subject_complexity[subject]
        else:
            # Default distribution for unknown subjects
            base_dist = {'reading': 0.4, 'practice': 0.4, 'revision': 0.2}
        
        # Apply scenario adjustments
        scenario_adj = self.scenario_adjustments.get(scenario, self.scenario_adjustments['general_study'])
        
        # Calculate adjusted time allocation
        reading_time = base_dist['reading'] * scenario_adj['reading'] * total_hours
        practice_time = base_dist['practice'] * scenario_adj['practice'] * total_hours
        revision_time = base_dist['revision'] * scenario_adj['revision'] * total_hours
        
        # Normalize to ensure total equals input hours
        total_calculated = reading_time + practice_time + revision_time
        if total_calculated > 0:
            reading_time = (reading_time / total_calculated) * total_hours
            practice_time = (practice_time / total_calculated) * total_hours
            revision_time = (revision_time / total_calculated) * total_hours
        
        return {
            'reading': round(reading_time, 1),
            'practice': round(practice_time, 1),
            'revision': round(revision_time, 1),
            'total': round(reading_time + practice_time + revision_time, 1)
        }
    
    def generate_daily_schedule(self, subject, daily_hours, scenario='general_study'):
        """Generate a detailed daily study schedule"""
        time_dist = self.calculate_time_distribution(subject, daily_hours, scenario)
        
        # Create time slots (assuming 30-minute minimum blocks)
        min_block = 0.5  # 30 minutes
        
        # Calculate number of blocks for each activity
        reading_blocks = max(1, round(time_dist['reading'] / min_block))
        practice_blocks = max(1, round(time_dist['practice'] / min_block))
        revision_blocks = max(1, round(time_dist['revision'] / min_block))
        
        # Create schedule with breaks
        schedule = []
        
        # Reading session
        if reading_blocks > 0:
            schedule.append({
                'activity': 'Reading',
                'duration': reading_blocks * min_block,
                'description': f'Read {subject} theory and concepts',
                'tips': ['Take notes while reading', 'Highlight key concepts', 'Ask questions about unclear topics']
            })
        
        # Short break
        if daily_hours > 1:
            schedule.append({
                'activity': 'Break',
                'duration': 0.25,
                'description': 'Short break - stretch, hydrate',
                'tips': ['Step away from study area', 'Do light physical activity']
            })
        
        # Practice session
        if practice_blocks > 0:
            schedule.append({
                'activity': 'Practice',
                'duration': practice_blocks * min_block,
                'description': f'Solve {subject} problems and exercises',
                'tips': ['Start with easier problems', 'Time yourself', 'Check solutions carefully']
            })
        
        # Another break for longer sessions
        if daily_hours > 2:
            schedule.append({
                'activity': 'Break',
                'duration': 0.25,
                'description': 'Medium break - refresh mind',
                'tips': ['Get fresh air if possible', 'Have a healthy snack']
            })
        
        # Revision session
        if revision_blocks > 0:
            schedule.append({
                'activity': 'Revision',
                'duration': revision_blocks * min_block,
                'description': f'Review and consolidate {subject} learning',
                'tips': ['Summarize key points', 'Test yourself', 'Connect new concepts with previous knowledge']
            })
        
        return schedule
    
    def create_weekly_plan(self, subject, daily_hours, scenario='general_study', start_date=None):
        """Create a comprehensive 7-day study plan"""
        if start_date is None:
            start_date = datetime.now().date()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        weekly_plan = {
            'subject': subject,
            'scenario': scenario,
            'daily_hours': daily_hours,
            'total_weekly_hours': daily_hours * 7,
            'start_date': start_date.isoformat(),
            'time_distribution': self.calculate_time_distribution(subject, daily_hours * 7, scenario),
            'daily_schedules': {}
        }
        
        # Generate daily schedules
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, day in enumerate(days):
            current_date = start_date + timedelta(days=i)
            
            # Adjust daily hours based on day (lighter on weekends for general study)
            if scenario == 'general_study' and day in ['Saturday', 'Sunday']:
                adjusted_hours = daily_hours * 0.8
            elif scenario == 'exam_prep':
                adjusted_hours = daily_hours * 1.1 if day in ['Saturday', 'Sunday'] else daily_hours
            else:
                adjusted_hours = daily_hours
            
            daily_schedule = self.generate_daily_schedule(subject, adjusted_hours, scenario)
            
            weekly_plan['daily_schedules'][day] = {
                'date': current_date.isoformat(),
                'planned_hours': round(adjusted_hours, 1),
                'schedule': daily_schedule,
                'focus_areas': self.get_daily_focus_areas(subject, day, scenario)
            }
        
        return weekly_plan
    
    def get_daily_focus_areas(self, subject, day, scenario):
        """Get specific focus areas for each day"""
        focus_areas = {
            'Mathematics': {
                'Monday': ['Algebra fundamentals', 'Linear equations'],
                'Tuesday': ['Geometry concepts', 'Area and volume'],
                'Wednesday': ['Calculus basics', 'Derivatives'],
                'Thursday': ['Statistics', 'Probability'],
                'Friday': ['Problem-solving practice', 'Mixed exercises'],
                'Saturday': ['Review weak areas', 'Practice tests'],
                'Sunday': ['Comprehensive review', 'Prepare for next week']
            },
            'Physics': {
                'Monday': ['Mechanics', 'Newton\'s laws'],
                'Tuesday': ['Energy and momentum', 'Work and power'],
                'Wednesday': ['Waves and oscillations', 'Sound'],
                'Thursday': ['Electricity and magnetism', 'Circuits'],
                'Friday': ['Thermodynamics', 'Heat transfer'],
                'Saturday': ['Problem-solving', 'Laboratory concepts'],
                'Sunday': ['Review and integration', 'Conceptual understanding']
            },
            'Chemistry': {
                'Monday': ['Atomic structure', 'Periodic table'],
                'Tuesday': ['Chemical bonding', 'Molecular geometry'],
                'Wednesday': ['Chemical reactions', 'Stoichiometry'],
                'Thursday': ['Solutions and concentrations', 'Acids and bases'],
                'Friday': ['Organic chemistry basics', 'Functional groups'],
                'Saturday': ['Laboratory techniques', 'Safety procedures'],
                'Sunday': ['Review and practice', 'Concept connections']
            },
            'Biology': {
                'Monday': ['Cell structure and function', 'Organelles'],
                'Tuesday': ['Genetics and heredity', 'DNA and RNA'],
                'Wednesday': ['Evolution and natural selection', 'Species'],
                'Thursday': ['Ecology and ecosystems', 'Environmental science'],
                'Friday': ['Human anatomy and physiology', 'Body systems'],
                'Saturday': ['Laboratory skills', 'Microscopy'],
                'Sunday': ['Review and synthesis', 'Biological connections']
            },
            'Computer Science': {
                'Monday': ['Programming fundamentals', 'Syntax and logic'],
                'Tuesday': ['Data structures', 'Arrays and lists'],
                'Wednesday': ['Algorithms', 'Sorting and searching'],
                'Thursday': ['Object-oriented programming', 'Classes and objects'],
                'Friday': ['Database concepts', 'SQL basics'],
                'Saturday': ['Project work', 'Coding practice'],
                'Sunday': ['Code review', 'Debugging and testing']
            }
        }
        
        # Get subject-specific focus areas or use general ones
        if subject in focus_areas:
            return focus_areas[subject].get(day, ['General study', 'Review concepts'])
        else:
            return ['Core concepts', 'Practice exercises', 'Review materials']
    
    def save_study_plan_csv(self, weekly_plan, filename=None):
        """Save study plan as downloadable CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Use absolute path to ensure it works from any directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            outputs_dir = os.path.join(base_dir, 'outputs')
            filename = os.path.join(outputs_dir, f'study_plan_{weekly_plan["subject"]}_{timestamp}.csv')
        
        # Create CSV data
        csv_data = []
        
        for day, day_data in weekly_plan['daily_schedules'].items():
            for i, activity in enumerate(day_data['schedule']):
                csv_data.append({
                    'Day': day,
                    'Date': day_data['date'],
                    'Activity_Order': i + 1,
                    'Activity': activity['activity'],
                    'Duration_Hours': activity['duration'],
                    'Description': activity['description'],
                    'Tips': '; '.join(activity.get('tips', [])),
                    'Focus_Areas': '; '.join(day_data['focus_areas'])
                })
        
        # Create DataFrame and save
        df = pd.DataFrame(csv_data)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        
        print(f"✓ Study plan saved to {filename}")
        return filename
    
    def generate_study_recommendations(self, subject, available_hours, scenario):
        """Generate personalized study recommendations"""
        recommendations = []
        
        # Time-based recommendations
        if available_hours < 1:
            recommendations.append("Consider increasing study time to at least 1 hour daily for effective learning")
        elif available_hours > 4:
            recommendations.append("Break long study sessions into smaller chunks with regular breaks")
        
        # Subject-specific recommendations
        subject_tips = {
            'Mathematics': [
                "Focus heavily on practice problems - math requires doing, not just reading",
                "Keep a formula sheet and review it daily",
                "Work through problems step-by-step, don't skip steps"
            ],
            'Physics': [
                "Always draw diagrams for physics problems",
                "Understand the physical meaning behind equations",
                "Practice dimensional analysis to check your work"
            ],
            'Chemistry': [
                "Memorize the periodic table early in your studies",
                "Practice balancing chemical equations regularly",
                "Connect molecular structure to chemical properties"
            ],
            'Biology': [
                "Use concept maps to connect biological processes",
                "Create mnemonics for complex biological terms",
                "Study at different organizational levels (molecular to ecosystem)"
            ],
            'Computer Science': [
                "Code every day, even if just for 30 minutes",
                "Debug systematically - don't guess and check",
                "Read other people's code to learn different approaches"
            ]
        }
        
        if subject in subject_tips:
            recommendations.extend(random.sample(subject_tips[subject], 2))
        
        # Scenario-specific recommendations
        if scenario == 'exam_prep':
            recommendations.extend([
                "Create a countdown calendar to your exam date",
                "Take practice tests under timed conditions",
                "Focus extra time on your weakest topics"
            ])
        elif scenario == 'homework':
            recommendations.extend([
                "Start assignments early to avoid last-minute stress",
                "Break large assignments into smaller, manageable tasks"
            ])
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def create_comprehensive_plan(self, subject, daily_hours, scenario='general_study', start_date=None):
        """Create a comprehensive study plan with all components"""
        # Generate weekly plan
        weekly_plan = self.create_weekly_plan(subject, daily_hours, scenario, start_date)
        
        # Add recommendations
        weekly_plan['recommendations'] = self.generate_study_recommendations(subject, daily_hours, scenario)
        
        # Add summary statistics
        total_reading = sum(day['schedule'][0]['duration'] for day in weekly_plan['daily_schedules'].values() 
                          if day['schedule'] and day['schedule'][0]['activity'] == 'Reading')
        total_practice = sum(activity['duration'] for day in weekly_plan['daily_schedules'].values() 
                           for activity in day['schedule'] if activity['activity'] == 'Practice')
        total_revision = sum(activity['duration'] for day in weekly_plan['daily_schedules'].values() 
                           for activity in day['schedule'] if activity['activity'] == 'Revision')
        
        weekly_plan['summary'] = {
            'total_study_hours': round(total_reading + total_practice + total_revision, 1),
            'reading_hours': round(total_reading, 1),
            'practice_hours': round(total_practice, 1),
            'revision_hours': round(total_revision, 1),
            'average_daily_hours': round((total_reading + total_practice + total_revision) / 7, 1)
        }
        
        return weekly_plan

# Example usage and testing
if __name__ == "__main__":
    # Initialize study planner
    planner = StudyPlanner()
    
    # Create comprehensive study plan
    study_plan = planner.create_comprehensive_plan(
        subject="Mathematics",
        daily_hours=3,
        scenario="exam_prep",
        start_date="2024-01-15"
    )
    
    print("📅 Study Plan Generated:")
    print(f"Subject: {study_plan['subject']}")
    print(f"Scenario: {study_plan['scenario']}")
    print(f"Total weekly hours: {study_plan['summary']['total_study_hours']}")
    print(f"Daily average: {study_plan['summary']['average_daily_hours']} hours")
    
    print(f"\n⏰ Time Distribution:")
    print(f"Reading: {study_plan['summary']['reading_hours']} hours")
    print(f"Practice: {study_plan['summary']['practice_hours']} hours")
    print(f"Revision: {study_plan['summary']['revision_hours']} hours")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(study_plan['recommendations'], 1):
        print(f"{i}. {rec}")
    
    # Save as CSV
    csv_file = planner.save_study_plan_csv(study_plan)
    
    # Save as JSON for web app
    json_file = 'outputs/study_plan_sample.json'
    os.makedirs('outputs', exist_ok=True)
    with open(json_file, 'w') as f:
        json.dump(study_plan, f, indent=2, default=str)
    
    print(f"✓ Study plan also saved as JSON: {json_file}")
    print("\n✓ Study Planning module completed!")