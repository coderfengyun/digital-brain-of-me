# Operations Module

This module tracks your goals, tasks, meetings, and productivity metrics.

## Structure

### goals/
Define and track your goals at different time horizons in `goals.yaml`.

**Hierarchy:**
- Yearly goals (big picture)
- Quarterly goals (linked to yearly)
- Monthly goals (linked to quarterly)

### tasks/
Day-to-day action items in `tasks.jsonl`.

**Format:**
```json
{
  "id": "task-XXX",
  "title": "Task description",
  "description": "Detailed description",
  "status": "todo|in_progress|done|blocked",
  "priority": "low|medium|high",
  "created_at": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "tags": ["tag1", "tag2"],
  "related_goal": "goal reference"
}
```

### meetings/
Meeting notes and action items in `meetings.jsonl`.

**Format:**
```json
{
  "id": "meeting-XXX",
  "title": "Meeting title",
  "date": "YYYY-MM-DD",
  "attendees": ["person1", "person2"],
  "agenda": "What was discussed",
  "notes": "Key points and decisions",
  "action_items": ["action1", "action2"],
  "follow_up": "Next steps"
}
```

### metrics/
Weekly productivity metrics in `weekly.jsonl`.

**Format:**
```json
{
  "week_of": "YYYY-MM-DD",
  "content_published": 0,
  "new_contacts": 0,
  "meetings": 0,
  "learning_hours": 0,
  "tasks_completed": 0,
  "notes": "Reflections on the week"
}
```

## Usage Tips

- Link tasks to goals to ensure alignment
- Review goals weekly/monthly to track progress
- Use metrics to identify patterns and optimize productivity
- Extract action items from meetings into tasks
