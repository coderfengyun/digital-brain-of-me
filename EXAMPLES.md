# Usage Examples

Real-world scenarios showing how to use your Digital Brain.

## Example 1: Daily Content Creator

### Morning Routine (5 min)

**1. Review yesterday's progress**
```bash
python scripts/weekly_review.py
```

**2. Check content ideas**
```bash
python scripts/content_ideas.py
```

**3. Pick an idea and start drafting**
```bash
python scripts/idea_to_draft.py idea-042
```

### During the Day

**Save interesting articles** (as you browse):
```bash
# Via Claude Code
"Save this article about AI: https://example.com/ai-article"
```

**Capture quick ideas**:
```bash
# Via Claude Code
"Add content idea: How AI is changing knowledge management"
```

### Evening Review (3 min)

**Log what you published**:
```bash
echo '{"id": "post-010", "title": "My AI workflow", "url": "https://myblog.com/ai-workflow", "platform": "blog", "published_at": "2026-02-26", "tags": ["AI", "productivity"], "original_idea_id": "idea-042"}' >> content/published/published.jsonl
```

**Update metrics** (automatic via weekly_review.py)

---

## Example 2: Developer Building Network

### After Attending Conference

**Add new contacts**:
```bash
# Via Claude Code
"Add Sarah Chen as a contact - met at AI Summit, works at OpenAI on agents"
"Add Marcus Johnson - colleague from Google, interested in LLMs"
"Add Dr. Kim Lee - professor at Stanford, researching AI safety"
```

This creates:
```jsonl
{"id": "contact-010", "name": "Sarah Chen", "relationship": "colleague", "tags": ["AI", "agents", "OpenAI"], "met_at": "2026-02-26", "last_contact": "2026-02-26", "notes": "Met at AI Summit, works at OpenAI on agents", "links": {"twitter": "@sarahchen", "linkedin": "sarah-chen", "email": "sarah@openai.com"}}
```

### Weekly Network Maintenance

**Check who to reach out to**:
```bash
python scripts/stale_contacts.py
```

Output:
```
# Contacts to Reach Out To
==================================================

## High Priority (30-60 days)

### Sarah Chen
  Relationship: colleague
  Last contact: 45 days ago
  Notes: Met at AI Summit, works at OpenAI on agents

### Marcus Johnson
  Relationship: colleague
  Last contact: 38 days ago
  Notes: Colleague from Google, interested in LLMs
```

**Log interactions**:
```bash
echo '{"id": "interaction-023", "contact_id": "contact-010", "date": "2026-02-26", "type": "email", "summary": "Followed up on AI agents discussion, shared my latest blog post", "follow_up": "She mentioned wanting to collaborate - schedule call next week"}' >> network/relationships/interactions.jsonl
```

---

## Example 3: Student Learning New Technology

### Starting to Learn Rust

**Set up learning goal**:

Edit `operations/goals/goals.yaml`:
```yaml
yearly_goals:
  - goal: "Become proficient in Rust"
    category: "learning"
    status: "in_progress"
    target_date: "2026-12-31"
    progress: 10
    milestones:
      - "Complete Rust book"
      - "Build 3 projects"
      - "Contribute to open source"

quarterly_goals:
  - goal: "Complete Rust fundamentals"
    quarter: "Q1"
    year: 2026
    status: "in_progress"
    progress: 30
    related_yearly_goal: "Become proficient in Rust"
```

**Track learning resources**:

Edit `knowledge/learning/courses.yaml`:
```yaml
books:
  - title: "The Rust Programming Language"
    author: "Steve Klabnik and Carol Nichols"
    status: "reading"
    started_at: "2026-02-01"
    completed_at: ""
    key_takeaways:
      - "Ownership system prevents memory bugs"
      - "Borrowing rules enable safe concurrency"
    rating: 0

courses:
  - title: "Rust by Example"
    platform: "rust-lang.org"
    status: "in_progress"
    started_at: "2026-02-10"
    notes: "Great hands-on examples"
    tags: ["rust", "programming"]
```

### Daily Learning Workflow

**Save useful resources**:
```bash
# As you find them
echo '{"id": "bm-050", "url": "https://doc.rust-lang.org/book/", "title": "The Rust Book", "description": "Official Rust programming language book", "tags": ["rust", "tutorial", "documentation"], "saved_at": "2026-02-26", "category": "documentation"}' >> knowledge/bookmarks/bookmarks.jsonl
```

**Take research notes**:

Edit `knowledge/research/notes.md`:
```markdown
## Rust Ownership System

### Key Findings
- Each value has a single owner
- Ownership can be transferred (moved)
- References allow borrowing without ownership
- Compiler enforces at compile-time

### Sources
- Bookmark bm-050 (The Rust Book, Chapter 4)
- Bookmark bm-051 (Understanding Ownership blog post)

### Date
2026-02-26

### My Thoughts
This is fundamentally different from garbage collection.
Could be great for systems programming where performance matters.
Need to practice more with borrowing patterns.
```

**Track progress**:
```bash
echo '{"id": "task-105", "title": "Complete Chapter 4 exercises", "description": "Ownership exercises in Rust book", "status": "done", "priority": "medium", "created_at": "2026-02-26", "due_date": "", "tags": ["rust", "learning"], "related_goal": "Become proficient in Rust"}' >> operations/tasks/tasks.jsonl
```

---

## Example 4: Researcher Managing Projects

### Starting New Research Project

**Capture initial idea**:
```bash
echo '{"id": "idea-088", "title": "Context engineering for AI agents", "description": "Research paper on optimal context management strategies", "tags": ["AI", "research", "context-engineering"], "status": "new", "created_at": "2026-02-26", "priority": "high"}' >> content/ideas/ideas.jsonl
```

**Collect related papers**:
```bash
# Save each paper as bookmark
echo '{"id": "bm-120", "url": "https://arxiv.org/abs/2304.xxxxx", "title": "Attention Is All You Need", "description": "Transformer architecture paper", "tags": ["AI", "transformers", "research"], "saved_at": "2026-02-26", "category": "paper"}' >> knowledge/bookmarks/bookmarks.jsonl

echo '{"id": "bm-121", "url": "https://arxiv.org/abs/2305.xxxxx", "title": "ReAct: Reasoning and Acting", "description": "Agent reasoning framework", "tags": ["AI", "agents", "reasoning"], "saved_at": "2026-02-26", "category": "paper"}' >> knowledge/bookmarks/bookmarks.jsonl
```

**Create research notes**:

Create `knowledge/research/context-engineering.md`:
```markdown
# Context Engineering Research

## Research Question
How can AI agents optimally manage their context window to maximize task performance?

## Related Work

### Paper 1: Attention Mechanisms (bm-120)
- Transformers use self-attention
- Context window limited by O(n²) complexity
- Key insight: Not all context equally important

### Paper 2: ReAct Framework (bm-121)
- Interleaving reasoning and action
- Context includes: task, observations, thoughts, actions
- Performance degrades with irrelevant context

## Hypothesis
Progressive context loading based on task type will outperform full context loading.

## Methodology
1. Define task categories
2. Map optimal context per category
3. Benchmark against baseline
4. Analyze results

## Next Steps
- [ ] Literature review (10 more papers)
- [ ] Design experiment
- [ ] Implement prototype
- [ ] Run benchmarks
```

**Track tasks**:
```bash
# Add research tasks
echo '{"id": "task-200", "title": "Complete literature review", "description": "Read and summarize 10 papers on context management", "status": "in_progress", "priority": "high", "created_at": "2026-02-26", "due_date": "2026-03-15", "tags": ["research", "reading"], "related_goal": ""}' >> operations/tasks/tasks.jsonl
```

---

## Example 5: Professional Managing Career

### Career Goals Setup

Edit `operations/goals/goals.yaml`:
```yaml
yearly_goals:
  - goal: "Get promoted to Senior Engineer"
    category: "career"
    status: "in_progress"
    target_date: "2026-12-31"
    progress: 40
    milestones:
      - "Lead 2 major projects"
      - "Mentor 3 junior engineers"
      - "Present at 1 conference"
      - "Publish 5 technical articles"

quarterly_goals:
  - goal: "Lead project X to completion"
    quarter: "Q1"
    year: 2026
    status: "in_progress"
    progress: 60
    related_yearly_goal: "Get promoted to Senior Engineer"

  - goal: "Publish 2 technical articles"
    quarter: "Q1"
    year: 2026
    status: "in_progress"
    progress: 50
    related_yearly_goal: "Get promoted to Senior Engineer"
```

### Weekly Review Ritual

**Every Sunday evening**:

```bash
# 1. Generate review
python scripts/weekly_review.py
```

Output:
```
# Weekly Review - Week of 2026-02-24
==================================================

## Tasks Completed: 12
  - Complete API refactoring
  - Review team PRs
  - Write blog post draft
  - Mentor session with junior dev
  ...

## Content Published: 1
  - "Optimizing React Performance" (blog)

## New Contacts: 2
  - Alex Rivera (conference speaker)
  - Jordan Wu (potential mentor)

## Meetings: 5
  - Team standup (daily)
  - 1:1 with manager
  - Project kickoff

## Summary
  - Total tasks completed: 12
  - Content pieces published: 1
  - New connections made: 2
  - Meetings attended: 5
```

**Reflect and plan**:
```bash
# 2. Check goal progress
# Update progress percentages in goals.yaml

# 3. Check relationships
python scripts/stale_contacts.py

# 4. Plan content
python scripts/content_ideas.py
```

**Update goals**:
```yaml
quarterly_goals:
  - goal: "Lead project X to completion"
    quarter: "Q1"
    year: 2026
    status: "in_progress"
    progress: 75  # ← Updated from 60
    related_yearly_goal: "Get promoted to Senior Engineer"
```

---

## Example 6: Combining Multiple Modules

### Scenario: Writing Technical Article

**Step 1: Find topic** (Content + Knowledge)
```bash
python scripts/content_ideas.py
```

Identifies: "You have 8 bookmarks on 'performance-optimization' but no published content"

**Step 2: Gather research** (Knowledge)
```bash
# Via Claude Code
"Show me all bookmarks tagged 'performance-optimization'"
```

**Step 3: Create draft** (Content)
```bash
python scripts/idea_to_draft.py idea-099
```

Creates: `content/drafts/react-performance-optimization.md`

**Step 4: Write & edit** (Content)
```bash
# Edit the draft file
code content/drafts/react-performance-optimization.md
```

**Step 5: Get feedback** (Network)
```bash
# Via Claude Code
"Who in my network works with React? I want feedback on my article"
```

Suggests contacts to reach out to.

**Step 6: Publish & log** (Content + Operations)
```bash
# After publishing
echo '{"id": "post-042", "title": "React Performance Optimization Guide", "url": "https://myblog.com/react-perf", "platform": "blog", "published_at": "2026-02-26", "tags": ["react", "performance", "javascript"], "original_idea_id": "idea-099"}' >> content/published/published.jsonl

# Mark task complete
echo '{"id": "task-155", "title": "Write React performance article", "status": "done", "completed_at": "2026-02-26"}' >> operations/tasks/tasks.jsonl
```

**Step 7: Share with network** (Network)
```bash
# Log interactions
echo '{"id": "interaction-077", "contact_id": "contact-033", "date": "2026-02-26", "type": "message", "summary": "Shared my React performance article, they gave great feedback on useMemo section", "follow_up": ""}' >> network/relationships/interactions.jsonl
```

---

## Pro Tips

### 1. Use Claude Code for Quick Entry

Instead of manually writing JSON:
```bash
# Just say:
"Add bookmark for https://rust-lang.org tagged rust, programming, official"
"Add task: Review PR #123, due tomorrow, high priority"
"I met Alice at DevCon, she works on ML at Meta"
```

### 2. Batch Similar Operations

```bash
# Add multiple ideas at once
cat << EOF >> content/ideas/ideas.jsonl
{"id": "idea-201", "title": "Idea 1", ...}
{"id": "idea-202", "title": "Idea 2", ...}
{"id": "idea-203", "title": "Idea 3", ...}
EOF
```

### 3. Use Tags Consistently

Good tagging strategy:
- **Technology**: rust, python, javascript, react
- **Type**: tutorial, reference, tool, paper
- **Status**: learning, mastered, interested
- **Domain**: career, side-project, research

### 4. Regular Reviews

- **Daily**: Check tasks, add bookmarks
- **Weekly**: Run weekly_review.py, update goals
- **Monthly**: Review all modules, archive old data
- **Quarterly**: Assess goal progress, plan next quarter

### 5. Link Everything

When creating content, reference:
```markdown
# Article Draft

Based on research in notes.md
See bookmarks: bm-120, bm-121, bm-122
Related to goal: "Publish 5 technical articles"
For contact: Alex Rivera might be interested
```

---

## Advanced Workflows

### Automated Daily Capture

Create `scripts/daily_capture.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)

echo "=== Daily Capture - $DATE ==="
echo ""
echo "Quick entries (press Enter to skip):"
echo ""

read -p "Any ideas today? " idea
if [ -n "$idea" ]; then
  echo "{\"id\": \"idea-$(date +%s)\", \"title\": \"$idea\", \"created_at\": \"$DATE\", \"status\": \"new\", \"priority\": \"medium\", \"tags\": []}" >> content/ideas/ideas.jsonl
fi

read -p "Any tasks? " task
if [ -n "$task" ]; then
  echo "{\"id\": \"task-$(date +%s)\", \"title\": \"$task\", \"created_at\": \"$DATE\", \"status\": \"todo\", \"priority\": \"medium\", \"tags\": []}" >> operations/tasks/tasks.jsonl
fi

echo ""
echo "Captured to your Digital Brain!"
```

### Context-Aware Queries

```bash
# Find all content ideas related to current bookmarks
python scripts/suggest_content_from_recent_bookmarks.py

# Identify learning gaps
python scripts/find_knowledge_gaps.py

# Network value analysis
python scripts/analyze_network_influence.py
```

---

Ready to start using your Digital Brain? See [QUICKSTART.md](QUICKSTART.md) for setup instructions!
