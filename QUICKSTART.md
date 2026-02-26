# Quick Start Guide

Get your Digital Brain up and running in 5 minutes!

## Step 1: Fill in Your Identity (2 min)

### Your Profile
Edit [identity/brand/profile.yaml](identity/brand/profile.yaml):

```yaml
name: "Your Name"
tagline: "Your professional tagline"
bio: |
  Your professional biography

values:
  - "Value 1"
  - "Value 2"

expertise:
  - "Skill 1"
  - "Skill 2"
```

### Your Voice
Edit [identity/voice/style.md](identity/voice/style.md) with your writing preferences.

## Step 2: Try Adding Data (2 min)

### Option A: Manual (Copy-Paste)

Add a content idea:
```bash
echo '{"id": "idea-002", "title": "My first digital brain idea", "description": "Test entry", "tags": ["test"], "status": "new", "created_at": "2026-02-26", "priority": "medium"}' >> content/ideas/ideas.jsonl
```

Add a bookmark:
```bash
echo '{"id": "bm-002", "url": "https://github.com", "title": "GitHub", "description": "Code hosting platform", "tags": ["tools", "dev"], "saved_at": "2026-02-26", "category": "tool"}' >> knowledge/bookmarks/bookmarks.jsonl
```

Add a task:
```bash
echo '{"id": "task-002", "title": "Set up my digital brain", "description": "Complete initial setup", "status": "in_progress", "priority": "high", "created_at": "2026-02-26", "due_date": "", "tags": ["setup"], "related_goal": ""}' >> operations/tasks/tasks.jsonl
```

### Option B: Using Claude Code

Just chat with Claude:
- "Add a content idea about learning Python"
- "Save https://example.com to my bookmarks"
- "Add a task to review my goals"

## Step 3: Try Automation (1 min)

### Weekly Review
```bash
python scripts/weekly_review.py
```

### Content Ideas
```bash
python scripts/content_ideas.py
```

### Stale Contacts
```bash
python scripts/stale_contacts.py
```

## Step 4: Explore the Modules

### Content Pipeline
1. Add ideas → [content/ideas/ideas.jsonl](content/ideas/ideas.jsonl)
2. Create drafts → [content/drafts/](content/drafts/)
3. Log published → [content/published/published.jsonl](content/published/published.jsonl)

### Knowledge Base
- Bookmarks → [knowledge/bookmarks/bookmarks.jsonl](knowledge/bookmarks/bookmarks.jsonl)
- Research → [knowledge/research/notes.md](knowledge/research/notes.md)
- Learning → [knowledge/learning/courses.yaml](knowledge/learning/courses.yaml)

### Network
- Contacts → [network/contacts/contacts.jsonl](network/contacts/contacts.jsonl)
- Interactions → [network/relationships/interactions.jsonl](network/relationships/interactions.jsonl)

### Operations
- Goals → [operations/goals/goals.yaml](operations/goals/goals.yaml)
- Tasks → [operations/tasks/tasks.jsonl](operations/tasks/tasks.jsonl)
- Meetings → [operations/meetings/meetings.jsonl](operations/meetings/meetings.jsonl)

## Step 5: Make it Yours

### Customize
- Add your own scripts in `scripts/`
- Create custom modules for your needs
- Adjust data schemas as needed

### Best Practices
1. Update regularly (daily tasks, weekly reviews)
2. Tag consistently across modules
3. Link related items (tasks to goals, content to bookmarks)
4. Use Claude Code for quick data entry
5. Commit to git frequently

## Common Use Cases

### "I want to remember this article"
```
"Save this article: [URL]"
```
Claude will add it to your bookmarks.

### "I have an idea for a blog post"
```
"Add a content idea about [topic]"
```
Claude will add it to your ideas with proper tags.

### "I met someone interesting"
```
"Add [Name] as a contact, met at [event]"
```
Claude will create a contact entry.

### "What should I work on?"
```
"What should I write about next?"
"Who should I reach out to?"
"Generate my weekly review"
```
Claude will run the appropriate automation script.

## Troubleshooting

### Python scripts not working?
Make sure they're executable:
```bash
chmod +x scripts/*.py
```

### Can't find Claude skill?
The skill is automatically loaded from `.claude/skills/digital-brain/`

### Want to start fresh?
Just delete the JSONL files and they'll be recreated:
```bash
rm content/ideas/ideas.jsonl
rm knowledge/bookmarks/bookmarks.jsonl
# etc.
```

## Next Steps

1. Read the full [README.md](README.md)
2. Explore each module's README
3. Set up weekly review as a habit
4. Start capturing everything in your Digital Brain

---

**You're all set!** Start using your Digital Brain to capture, organize, and synthesize information.
