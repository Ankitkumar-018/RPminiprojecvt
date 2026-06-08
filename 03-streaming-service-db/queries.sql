-- ============================================================
-- Streaming Service — Key Queries
-- ============================================================

-- ─── Q1: Top 5 highest-rated content overall ────────────────
SELECT
    title,
    type,
    genre,
    rating AS imdb_rating
FROM content
ORDER BY rating DESC
LIMIT 5;

-- ─── Q2: Most watched content (by number of users who completed it) ─
SELECT
    c.title,
    c.type,
    COUNT(*) AS completed_by_users
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 1
GROUP BY wh.content_id
ORDER BY completed_by_users DESC
LIMIT 10;

-- ─── Q3: Recommendation — "Users who watched X also watched" ─
-- Example: Who watched Sacred Games (content_id=1)?
-- Then find other content those users completed.
SELECT
    c.title,
    c.genre,
    COUNT(DISTINCT wh.user_id) AS shared_viewers
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 1
  AND wh.user_id IN (
      SELECT user_id FROM watch_history WHERE content_id = 1 AND completed = 1
  )
  AND wh.content_id != 1
GROUP BY wh.content_id
ORDER BY shared_viewers DESC
LIMIT 5;

-- ─── Q4: Content with highest average user rating ────────────
SELECT
    c.title,
    c.type,
    ROUND(AVG(r.stars), 2)  AS avg_user_rating,
    COUNT(r.rating_id)       AS num_reviews
FROM ratings r
JOIN content c ON c.content_id = r.content_id
GROUP BY r.content_id
HAVING num_reviews >= 2
ORDER BY avg_user_rating DESC
LIMIT 10;

-- ─── Q5: What is in a user's watchlist that they haven't watched? ─
-- For user Arjun (user_id=1):
SELECT
    c.title,
    c.type,
    c.genre
FROM watchlist wl
JOIN content c ON c.content_id = wl.content_id
WHERE wl.user_id = 1
  AND wl.content_id NOT IN (
      SELECT content_id FROM watch_history WHERE user_id = 1
  );

-- ─── Q6: Genre popularity — which genre has the most completed views? ─
SELECT
    c.genre,
    COUNT(*) AS total_completions
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 1
GROUP BY c.genre
ORDER BY total_completions DESC;

-- ─── Q7: Users who haven't watched anything in last 30 days (churn risk) ─
SELECT
    u.name,
    u.email,
    u.plan,
    MAX(wh.watched_at) AS last_watched
FROM users u
LEFT JOIN watch_history wh ON wh.user_id = u.user_id
GROUP BY u.user_id
HAVING last_watched IS NULL
    OR last_watched < DATE('now', '-30 days');

-- ─── Q8: Content currently in-progress (partially watched, not done) ─
-- For all users, show what they started but haven't finished
SELECT
    u.name,
    c.title,
    wh.percent_watched || '%' AS progress
FROM watch_history wh
JOIN users u   ON u.user_id   = wh.user_id
JOIN content c ON c.content_id = wh.content_id
WHERE wh.completed = 0
  AND wh.percent_watched > 0
ORDER BY wh.percent_watched DESC;

-- ─── Q9: Trending content — most watched in last 7 days ─────
-- (Using all data since our seed is static; in real app use watched_at filter)
SELECT
    c.title,
    c.genre,
    COUNT(DISTINCT wh.user_id) AS unique_viewers
FROM watch_history wh
JOIN content c ON c.content_id = wh.content_id
GROUP BY wh.content_id
ORDER BY unique_viewers DESC
LIMIT 5;

-- ─── Q10: Premium plan users who haven't upgraded their usage ─
SELECT
    u.name,
    u.plan,
    COUNT(wh.history_id) AS total_watches
FROM users u
LEFT JOIN watch_history wh ON wh.user_id = u.user_id
WHERE u.plan = 'premium'
GROUP BY u.user_id
HAVING total_watches < 3
ORDER BY total_watches;

-- ─── Q11: Content available in Hindi with rating above 8 ────
SELECT title, genre, release_year, rating
FROM content
WHERE language = 'Hindi'
  AND rating > 8.0
ORDER BY rating DESC;

-- ─── Q12: How many episodes does each series have? ──────────
SELECT
    c.title,
    e.season,
    COUNT(e.episode_id) AS episode_count,
    SUM(e.duration_min) AS total_duration_min
FROM episodes e
JOIN content c ON c.content_id = e.content_id
GROUP BY c.content_id, e.season
ORDER BY c.title, e.season;
