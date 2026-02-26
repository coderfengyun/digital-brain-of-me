#!/usr/bin/env python3
"""
Stale Contacts Detector

Identifies contacts you haven't interacted with recently
and suggests who to reach out to.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

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

def find_stale_contacts(days_threshold=30):
    """Find contacts not contacted recently"""
    contacts = load_jsonl('network/contacts/contacts.jsonl')
    interactions = load_jsonl('network/relationships/interactions.jsonl')

    # Get last interaction date for each contact
    last_interactions = {}
    for interaction in interactions:
        contact_id = interaction.get('contact_id')
        interaction_date = datetime.fromisoformat(interaction.get('date', '2000-01-01'))

        if contact_id not in last_interactions or interaction_date > last_interactions[contact_id]:
            last_interactions[contact_id] = interaction_date

    # Find stale contacts
    now = datetime.now()
    threshold = now - timedelta(days=days_threshold)
    stale = []

    for contact in contacts:
        contact_id = contact.get('id')
        last_contact_str = contact.get('last_contact', '2000-01-01')
        last_contact = datetime.fromisoformat(last_contact_str)

        # Use most recent date from either contact record or interactions
        if contact_id in last_interactions:
            last_contact = max(last_contact, last_interactions[contact_id])

        if last_contact < threshold:
            days_since = (now - last_contact).days
            stale.append({
                'contact': contact,
                'days_since': days_since,
                'last_contact': last_contact
            })

    return sorted(stale, key=lambda x: x['days_since'], reverse=True)

def suggest_contacts_to_reach_out():
    """Generate list of contacts to reach out to"""
    print("# Contacts to Reach Out To")
    print("=" * 50)
    print()

    stale_contacts = find_stale_contacts(days_threshold=30)

    if not stale_contacts:
        print("Great! You're staying in touch with everyone.")
        return

    # Priority contacts (haven't talked in 30-60 days)
    priority = [c for c in stale_contacts if 30 <= c['days_since'] < 60]
    if priority:
        print("## High Priority (30-60 days)")
        for item in priority[:5]:
            contact = item['contact']
            print(f"\n### {contact.get('name', 'Unknown')}")
            print(f"  Relationship: {contact.get('relationship', 'unknown')}")
            print(f"  Last contact: {item['days_since']} days ago")
            print(f"  Notes: {contact.get('notes', 'No notes')}")
        print()

    # Very stale (60+ days)
    very_stale = [c for c in stale_contacts if c['days_since'] >= 60]
    if very_stale:
        print("## Need Attention (60+ days)")
        for item in very_stale[:5]:
            contact = item['contact']
            print(f"\n### {contact.get('name', 'Unknown')}")
            print(f"  Relationship: {contact.get('relationship', 'unknown')}")
            print(f"  Last contact: {item['days_since']} days ago")
            print(f"  Notes: {contact.get('notes', 'No notes')}")
        print()

    print("=" * 50)
    print(f"Total contacts to consider: {len(stale_contacts)}")
    print("\nSuggestion: Pick 2-3 people and send them a quick message today!")

if __name__ == '__main__':
    suggest_contacts_to_reach_out()
