# Network Module

This module helps you maintain and nurture professional relationships.

## Structure

### contacts/
Your professional network in `contacts.jsonl`.

**Format:**
```json
{
  "id": "contact-XXX",
  "name": "Full Name",
  "relationship": "colleague|mentor|client|friend|acquaintance",
  "tags": ["tag1", "tag2"],
  "met_at": "YYYY-MM-DD",
  "last_contact": "YYYY-MM-DD",
  "notes": "Context about this person",
  "links": {
    "twitter": "",
    "linkedin": "",
    "email": "",
    "website": ""
  }
}
```

### relationships/
Track interactions in `interactions.jsonl`.

**Format:**
```json
{
  "id": "interaction-XXX",
  "contact_id": "contact-XXX",
  "date": "YYYY-MM-DD",
  "type": "meeting|email|call|message|event",
  "summary": "What you discussed",
  "follow_up": "Any action items or follow-ups"
}
```

## Usage Tips

- Update `last_contact` date when you interact with someone
- Set reminders to follow up with contacts you haven't spoken to recently
- Tag contacts by context (work, industry, conference, etc.)
- Use interactions log to track relationship history and commitments
