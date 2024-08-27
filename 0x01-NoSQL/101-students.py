#!/usr/bin/env python3
"""
This module contains a Python function that returns all students sorted by average score.
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    The average score is part of each item returned with the key `averageScore`.
    """
    # Get all students
    students = mongo_collection.find()
    
    # Calculate average score and add it to each student's document
    results = []
    for student in students:
        # Extract scores from topics
        scores = [topic['score'] for topic in student.get('topics', [])]
        if scores:
            average_score = sum(scores) / len(scores)
        else:
            average_score = 0
        
        # Add average score to the student document
        student['averageScore'] = average_score
        results.append(student)
    
    # Sort students by average score in descending order
    sorted_results = sorted(results, key=lambda x: x['averageScore'], reverse=True)
    
    return sorted_results

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.my_db
    collection = db.students
    top_students_list = top_students(collection)
    for student in top_students_list:
        print(f"[{student.get('_id')}] {student.get('name')} => {student.get('averageScore')}")
