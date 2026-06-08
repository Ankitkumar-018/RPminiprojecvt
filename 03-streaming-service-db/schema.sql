-- ============================================================
-- Streaming Service Database Schema (Hotstar / Netflix Style)
-- ============================================================

-- Users of the platform
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    country       TEXT    NOT NULL DEFAULT 'India',
    plan          TEXT    NOT NULL CHECK(plan IN ('free', 'basic', 'standard', 'premium')),
    joined_at     TEXT    NOT NULL DEFAULT (DATE('now'))
);

-- Content catalogue (movies + shows share this table)
CREATE TABLE content (
    content_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT    NOT NULL,
    type          TEXT    NOT NULL CHECK(type IN ('movie', 'series', 'documentary')),
    genre         TEXT    NOT NULL,
    language      TEXT    NOT NULL DEFAULT 'English',
    release_year  INTEGER NOT NULL,
    rating        REAL    NOT NULL CHECK(rating BETWEEN 0 AND 10),
    duration_min  INTEGER,           -- NULL for series (has episodes)
    description   TEXT
);

-- Episodes (only for series)
CREATE TABLE episodes (
    episode_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id    INTEGER NOT NULL REFERENCES content(content_id),
    season        INTEGER NOT NULL DEFAULT 1,
    episode_num   INTEGER NOT NULL,
    title         TEXT    NOT NULL,
    duration_min  INTEGER NOT NULL
);

-- Which content a user has watched and how much
CREATE TABLE watch_history (
    history_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id           INTEGER NOT NULL REFERENCES users(user_id),
    content_id        INTEGER NOT NULL REFERENCES content(content_id),
    watched_at        TEXT    NOT NULL DEFAULT (DATETIME('now')),
    percent_watched   INTEGER NOT NULL DEFAULT 0 CHECK(percent_watched BETWEEN 0 AND 100),
    completed         INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1))
);

-- User ratings and reviews
CREATE TABLE ratings (
    rating_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(user_id),
    content_id    INTEGER NOT NULL REFERENCES content(content_id),
    stars         INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
    review        TEXT,
    rated_at      TEXT    NOT NULL DEFAULT (DATETIME('now')),
    UNIQUE(user_id, content_id)
);

-- User's saved/bookmarked content
CREATE TABLE watchlist (
    watchlist_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(user_id),
    content_id    INTEGER NOT NULL REFERENCES content(content_id),
    added_at      TEXT    NOT NULL DEFAULT (DATETIME('now')),
    UNIQUE(user_id, content_id)
);

-- Tags for content (Action, Romance, etc.) — many-to-many
CREATE TABLE tags (
    tag_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL UNIQUE
);

CREATE TABLE content_tags (
    content_id    INTEGER NOT NULL REFERENCES content(content_id),
    tag_id        INTEGER NOT NULL REFERENCES tags(tag_id),
    PRIMARY KEY(content_id, tag_id)
);
