# Project 3: Streaming Service DB — Approach & Planning

---

## Part A: Filled Example
> Read this before you start coding. This is how a database engineer thinks through the problem.

---

### Step 1 — Understand the Problem

**What exactly does this project need?**
- A database schema that models a streaming platform like Hotstar
- Real data to populate it
- SQL queries that answer business questions like recommendations and trending

**What real-world entities exist in a streaming service?**
Think about what "things" exist:
- Users (who have accounts and plans)
- Content (movies and series)
- Episodes (parts of a series)
- Watching activity (who watched what, and how much)
- Ratings (what users think of content)
- Saved items (watchlist)
- Genres/Tags (categories of content)

Each entity = one table.

---

### Step 2 — Questions to Ask Before Writing Code

- **Should movies and series be in separate tables or one table?**
  → One table with a `type` column (`movie` or `series`). They share most fields (title, genre, rating). Series just have episodes linked separately.

- **How do I store watch progress?**
  → A `watch_history` table with `user_id`, `content_id`, and `percent_watched`. This is a junction table between users and content.

- **What is a many-to-many relationship? Where does it appear here?**
  → A piece of content can have many tags (Action, Drama). A tag can apply to many content items. This needs a junction table: `content_tags(content_id, tag_id)`.

- **How do I prevent a user from rating the same content twice?**
  → `UNIQUE(user_id, content_id)` constraint on the `ratings` table.

- **What is a foreign key and why does it matter?**
  → A foreign key links a column in one table to the primary key of another. It prevents orphan records — you can't have a `watch_history` entry for a user that doesn't exist.

---

### Step 3 — Pseudo Code (Schema Design)

```
Think about each table and its columns BEFORE writing SQL.

TABLE users:
  user_id     → unique ID (primary key, auto-incremented)
  name        → text, required
  email       → text, required, must be unique
  country     → text, default 'India'
  plan        → text, must be one of: free / basic / standard / premium
  joined_at   → date, default today

TABLE content:
  content_id   → unique ID
  title        → text, required
  type         → must be: movie / series / documentary
  genre        → text
  language     → text, default 'English'
  release_year → integer
  rating       → decimal 0.0 to 10.0
  duration_min → integer or NULL (NULL for series — use episodes table instead)

TABLE episodes:
  episode_id   → unique ID
  content_id   → FOREIGN KEY → content.content_id
  season       → integer
  episode_num  → integer
  title        → text
  duration_min → integer

TABLE watch_history:
  history_id       → unique ID
  user_id          → FOREIGN KEY → users.user_id
  content_id       → FOREIGN KEY → content.content_id
  watched_at       → datetime
  percent_watched  → integer 0–100
  completed        → boolean (0 or 1)

TABLE ratings:
  rating_id    → unique ID
  user_id      → FOREIGN KEY → users.user_id
  content_id   → FOREIGN KEY → content.content_id
  stars        → integer 1–5
  review       → text (optional)
  UNIQUE constraint on (user_id, content_id)  ← one rating per user per content
```

---

### Step 4 — Plan the Recommendation Query Before Writing SQL

**Business question:** "Users who watched Sacred Games also watched..."

**Think through it in English first:**
1. Find all users who completed Sacred Games
2. Find all other content those same users also completed
3. Count how many of those users watched each other content
4. Sort by that count (most shared viewers first)

**Then translate to SQL:**
```sql
-- Step 1: inner query finds users who watched Sacred Games
SELECT user_id FROM watch_history
WHERE content_id = 1 AND completed = 1

-- Step 2 + 3 + 4: outer query uses those users
SELECT c.title, COUNT(DISTINCT wh.user_id) AS shared_viewers
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.user_id IN (... step 1 ...)
  AND wh.content_id != 1
  AND wh.completed = 1
GROUP BY wh.content_id
ORDER BY shared_viewers DESC;
```

Always write the English logic first. Then write SQL.

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| FOREIGN KEY violation | Insert parent records before child records (users before watch_history) |
| UNIQUE constraint violation | Don't insert duplicate ratings — check before inserting |
| NULL in aggregation | `COUNT()` ignores NULLs — know which rows have NULLs |
| Query returns 0 rows | Check if the filter (WHERE) is too restrictive |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start writing SQL.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Identify the Entities

**List all the real-world "things" in a streaming service that need a table:**

```
1.
2.
3.
4.
5.
6.
```

---

### Step 2 — Design One Table (your choice)

Pick any table and list all its columns with data type and constraints:

```
TABLE NAME: _______________

Column name     | Data type | Constraints (NOT NULL, UNIQUE, FK, etc.)
----------------|-----------|------------------------------------------
                |           |
                |           |
                |           |
                |           |
```

---

### Step 3 — Identify Relationships

**Which tables have a one-to-many relationship? Give 2 examples:**

```
Example 1: _____________ has many _____________
Example 2: _____________ has many _____________
```

**Which tables have a many-to-many relationship? How do you handle it?**

```
Write here:


```

---

### Step 4 — Write the Recommendation Query in English First

Before writing SQL, write the recommendation logic in plain English steps:

```
Step 1:
Step 2:
Step 3:
Step 4:
```

Now try writing it in SQL:

```sql
-- Write your SQL here:


```

---

### Step 5 — Questions You Had Before Starting

```
1.
2.
3.
```

---

### Step 6 — After finishing, reflect

**What is the difference between WHERE and HAVING?**
```

```

**What does JOIN do? In your own words:**
```

```

**Which query was hardest to write and why?**
```

```
