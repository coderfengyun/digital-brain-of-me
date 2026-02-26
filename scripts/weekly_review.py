#!/usr/bin/env python3
"""
Weekly Review Generator

Generates a summary of your week by analyzing:
- Tasks completed
- Content published
- New contacts made
- Meetings attended
- Learning progress
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

def get_week_start(date=None):
    """Get the Monday of the current week"""
    if date is None:
        date = datetime.now()
    return date - timedelta(days=date.weekday())

def load_jsonl(filepath):
    """Load JSONL file and return list of records"""
    records = []
    if not Path(filepath).exists():
        return records

    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records

def filter_by_week(records, date_field, week_start):
    """Filter records that fall within the week"""
    week_end = week_start + timedelta(days=7)
    filtered = []

    for record in records:
        if date_field in record:
            record_date = datetime.fromisoformat(record[date_field].split('T')[0])
            if week_start <= record_date < week_end:
                filtered.append(record)

    return filtered

def generate_weekly_review():
    """Generate weekly review from all modules"""
    week_start = get_week_start()
    week_str = week_start.strftime('%Y-%m-%d')

    print(f"# Weekly Review - Week of {week_str}")
    print("=" * 50)
    print()

    # Tasks completed
    tasks = load_jsonl('operations/tasks/tasks.jsonl')
    completed_tasks = [t for t in tasks if t.get('status') == 'done']
    completed_this_week = filter_by_week(completed_tasks, 'created_at', week_start)

    print(f"## Tasks Completed: {len(completed_this_week)}")
    for task in completed_this_week:
        print(f"  - {task.get('title', 'Untitled')}")
    print()

    # Content published
    published = load_jsonl('content/published/published.jsonl')
    published_this_week = filter_by_week(published, 'published_at', week_start)

    print(f"## Content Published: {len(published_this_week)}")
    for item in published_this_week:
        print(f"  - {item.get('title', 'Untitled')} ({item.get('platform', 'unknown')})")
    print()

    # New contacts
    contacts = load_jsonl('network/contacts/contacts.jsonl')
    new_contacts = filter_by_week(contacts, 'met_at', week_start)

    print(f"## New Contacts: {len(new_contacts)}")
    for contact in new_contacts:
        print(f"  - {contact.get('name', 'Unknown')} ({contact.get('relationship', 'unknown')})")
    print()

    # Meetings
    meetings = load_jsonl('operations/meetings/meetings.jsonl')
    meetings_this_week = filter_by_week(meetings, 'date', week_start)

    print(f"## Meetings: {len(meetings_this_week)}")
    for meeting in meetings_this_week:
        print(f"  - {meeting.get('title', 'Untitled')}")
    print()

    # Summary metrics
    print("## Summary")
    print(f"  - Total tasks completed: {len(completed_this_week)}")
    print(f"  - Content pieces published: {len(published_this_week)}")
    print(f"  - New connections made: {len(new_contacts)}")
    print(f"  - Meetings attended: {len(meetings_this_week)}")
    print()

    # Save metrics
    metrics_file = 'operations/metrics/weekly.jsonl'
    metric_entry = {
        "week_of": week_str,
        "content_published": len(published_this_week),
        "new_contacts": len(new_contacts),
        "meetings": len(meetings_this_week),
        "tasks_completed": len(completed_this_week),
        "notes": ""
    }

    with open(metrics_file, 'a') as f:
        f.write(json.dumps(metric_entry) + '\n')

    print(f"Metrics saved to {metrics_file}")

if __name__ == '__main__':
    generate_weekly_review()
