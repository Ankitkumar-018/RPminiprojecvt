# Project 3: Streaming Service Schema and Queries

## What Is This?

A complete database design for a streaming platform (like Hotstar or Netflix), built with SQLite. Includes real seed data, a full schema with 8 tables, and 12 SQL queries that answer real business questions — including a recommendation engine.

---

## What Skills You Will Learn

- Relational database design from scratch (schema design)
- Primary keys, foreign keys, and constraints
- SQL JOINs — INNER JOIN, LEFT JOIN
- Aggregation — `GROUP BY`, `COUNT`, `AVG`, `SUM`
- Subqueries (queries inside queries)
- Recommendation logic written entirely in SQL
- Running SQL from Python using `sqlite3`

---

## How the System Works

```
schema.sql  (CREATE TABLE statements)
     │
     ▼
seed_data.sql  (INSERT statements — 10 users, 15 movies/series)
     │
     ▼
SQLite database file: streaming.db
     │
     ▼
queries.sql  (12 business queries)
     │
     ├── Q1: Top rated content
     ├── Q2: Most watched content
     ├── Q3: "Users who watched X also watched" (recommendation)
     ├── Q4: Highest user ratings
     ├── Q5: Unwatched watchlist items
     ├── Q6: Genre popularity
     ├── Q7: Churn risk (inactive users)
     ├── Q8: In-progress content
     ├── Q9: Trending content
     ├── Q10: Underutilising premium users
     ├── Q11: Language-filtered content
     └── Q12: Episodes per season
          │
          ▼
   Results printed to terminal
```

---

## Folder Structure

```
03-streaming-service-db/
├── schema.sql        ← CREATE TABLE statements (the database design)
├── seed_data.sql     ← INSERT statements (sample data)
├── queries.sql       ← All 12 queries with comments
├── run_queries.py    ← Python script: creates DB + runs queries + prints results
└── README.md
```

After running, this file is created:
```
└── streaming.db      ← The SQLite database file (auto-generated)
```

---

## Database Design (ER Diagram)

```
users
  │
  ├──< watch_history >── content
  ├──< ratings       >── content
  └──< watchlist     >── content
                            │
                            ├──< episodes
                            └──< content_tags >── tags
```

### Tables

| Table | Purpose |
|-------|---------|
| `users` | Platform subscribers (free / basic / standard / premium plans) |
| `content` | Movies, series, and documentaries catalogue |
| `episodes` | Individual episodes for series (linked to content) |
| `watch_history` | What each user watched and how much they completed (%) |
| `ratings` | User star ratings (1–5) and text reviews |
| `watchlist` | User's saved / bookmarked content |
| `tags` | Genre/mood labels (Action, Comedy, Finance, etc.) |
| `content_tags` | Many-to-many link between content and tags |

---

## Requirements

- Python 3.7 or higher
- SQLite3 — comes built-in with Python, no installation needed
- Optional: [DB Browser for SQLite](https://sqlitebrowser.org/) — free GUI to visually explore the database

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 03-streaming-service-db
```

### Step 2 — Run the Python script

```bash
python run_queries.py
```

This single command:
1. Creates `streaming.db`
2. Runs `schema.sql` (creates all 8 tables)
3. Runs `seed_data.sql` (inserts all users, content, and watch data)
4. Runs all 8 key queries
5. Prints results as formatted tables

### Step 3 — Explore the database interactively

```bash
sqlite3 streaming.db
```

Then try these commands inside SQLite:
```sql
.tables
SELECT * FROM content;
SELECT * FROM users;
SELECT title, rating FROM content ORDER BY rating DESC;
.quit
```

### Step 4 — Run all 12 queries directly from the SQL file

```bash
sqlite3 streaming.db < queries.sql
```

---

## Expected Output (Sample)

```
============================================================
  Q1: Top 5 Highest-Rated Content
============================================================
+--------------+--------+----------------+-------------+
| title        | type   | genre          | imdb_rating |
+--------------+--------+----------------+-------------+
| Scam 1992    | series | Finance/Drama  | 9.3         |
| Sacred Games | series | Crime/Thriller | 8.8         |
| Panchayat    | series | Comedy/Drama   | 8.8         |
| Mirzapur     | series | Crime/Drama    | 8.5         |
| Delhi Crime  | series | Crime/Drama    | 8.5         |
+--------------+--------+----------------+-------------+
  (5 rows)

============================================================
  Q3: Recommendation — 'Watched Sacred Games? Also watch...'
============================================================
+-------------+---------------+----------------+
| title       | genre         | shared_viewers |
+-------------+---------------+----------------+
| Scam 1992   | Finance/Drama | 3              |
| Delhi Crime | Crime/Drama   | 1              |
| Panchayat   | Comedy/Drama  | 1              |
+-------------+---------------+----------------+
  (3 rows)
```

---

## How the Key Queries Work

### Recommendation Query (Q3) — Collaborative Filtering

```sql
SELECT c.title, COUNT(DISTINCT wh.user_id) AS shared_viewers
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 1
  AND wh.user_id IN (
      -- find all users who completed Sacred Games
      SELECT user_id FROM watch_history WHERE content_id = 1 AND completed = 1
  )
  AND wh.content_id != 1   -- exclude Sacred Games itself
GROUP BY wh.content_id
ORDER BY shared_viewers DESC;
```

**Logic:** Find everyone who watched Sacred Games → see what else those same users watched → rank by how many of them watched it. This is the same idea behind "Users who bought X also bought Y" on Amazon.

### Genre Popularity (Q6)

```sql
SELECT c.genre, COUNT(*) AS total_completions
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 1
GROUP BY c.genre
ORDER BY total_completions DESC;
```

---

## The 12 Queries Explained

| # | Query | Real Business Use |
|---|-------|------------------|
| Q1 | Top rated content | Homepage "Top Picks" section |
| Q2 | Most completed content | Trending / popular content |
| Q3 | "Users who watched X also watched" | Collaborative filtering recommendation |
| Q4 | Highest user-rated content | User reviews leaderboard |
| Q5 | Watchlist not yet watched | "Resume where you left off" prompts |
| Q6 | Genre popularity | Content acquisition decisions |
| Q7 | Inactive users (30+ days) | Churn prevention emails |
| Q8 | In-progress content | "Continue watching" section |
| Q9 | Trending (unique viewers) | Trending section on homepage |
| Q10 | Underutilising premium users | Re-engagement campaigns |
| Q11 | Hindi content above 8.0 | Language-filtered browse page |
| Q12 | Episodes per season | Series details page |

---

## Try It Yourself — Extension Ideas

- Add a `subscriptions` table with start date, end date, and billing amount
- Write a query: "What are the new releases in the last 30 days?"
- Insert your own favourite movie and trace it through all tables
- Connect to a real dataset from Kaggle (IMDb movies CSV)
- Try the same schema in PostgreSQL or MySQL

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `no such table` | Running a query before creating the schema | Always run `python run_queries.py` first — it creates the DB |
| `FOREIGN KEY constraint failed` | Inserting a wrong ID in a child table | Check the parent table to confirm the ID exists |
| `UNIQUE constraint failed` | Inserting duplicate entry in ratings or watchlist | Each user can rate each content only once |
| `sqlite3: command not found` | SQLite CLI not installed | Skip Step 3 and use `python run_queries.py` only |
