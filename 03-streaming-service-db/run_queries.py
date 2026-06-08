import sqlite3
import os

DB_FILE = "streaming.db"


def setup_database():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")

    with open("schema.sql", "r") as f:
        conn.executescript(f.read())

    with open("seed_data.sql", "r") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def print_table(cursor, title):
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]

    col_widths = [max(len(str(col)), max((len(str(r[i])) for r in rows), default=0))
                  for i, col in enumerate(cols)]

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header = "| " + " | ".join(str(c).ljust(w) for c, w in zip(cols, col_widths)) + " |"

    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(sep)
    print(header)
    print(sep)
    for row in rows:
        print("| " + " | ".join(str(v).ljust(w) for v, w in zip(row, col_widths)) + " |")
    print(sep)
    print(f"  ({len(rows)} rows)\n")


def run_all_queries(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT title, type, genre, rating AS imdb_rating
        FROM content ORDER BY rating DESC LIMIT 5
    """)
    print_table(cur, "Q1: Top 5 Highest-Rated Content")

    cur.execute("""
        SELECT c.title, c.type, COUNT(*) AS completed_by_users
        FROM watch_history wh JOIN content c ON c.content_id = wh.content_id
        WHERE wh.completed = 1
        GROUP BY wh.content_id ORDER BY completed_by_users DESC LIMIT 10
    """)
    print_table(cur, "Q2: Most Watched Content (Completions)")

    cur.execute("""
        SELECT c.title, c.genre, COUNT(DISTINCT wh.user_id) AS shared_viewers
        FROM watch_history wh JOIN content c ON c.content_id = wh.content_id
        WHERE wh.completed = 1
          AND wh.user_id IN (
              SELECT user_id FROM watch_history WHERE content_id = 1 AND completed = 1)
          AND wh.content_id != 1
        GROUP BY wh.content_id ORDER BY shared_viewers DESC LIMIT 5
    """)
    print_table(cur, "Q3: Recommendation — 'Watched Sacred Games? Also watch...'")

    cur.execute("""
        SELECT c.title, ROUND(AVG(r.stars),2) AS avg_user_rating, COUNT(r.rating_id) AS reviews
        FROM ratings r JOIN content c ON c.content_id = r.content_id
        GROUP BY r.content_id HAVING reviews >= 2
        ORDER BY avg_user_rating DESC LIMIT 10
    """)
    print_table(cur, "Q4: Highest Average User Rating")

    cur.execute("""
        SELECT c.title, c.type, c.genre FROM watchlist wl
        JOIN content c ON c.content_id = wl.content_id
        WHERE wl.user_id = 1
          AND wl.content_id NOT IN (
              SELECT content_id FROM watch_history WHERE user_id = 1)
    """)
    print_table(cur, "Q5: Arjun's Watchlist — Not Yet Watched")

    cur.execute("""
        SELECT c.genre, COUNT(*) AS total_completions
        FROM watch_history wh JOIN content c ON c.content_id = wh.content_id
        WHERE wh.completed = 1 GROUP BY c.genre ORDER BY total_completions DESC
    """)
    print_table(cur, "Q6: Genre Popularity")

    cur.execute("""
        SELECT c.title, c.genre, COUNT(DISTINCT wh.user_id) AS unique_viewers
        FROM watch_history wh JOIN content c ON c.content_id = wh.content_id
        GROUP BY wh.content_id ORDER BY unique_viewers DESC LIMIT 5
    """)
    print_table(cur, "Q9: Trending — Most Unique Viewers")

    cur.execute("""
        SELECT title, genre, release_year, rating FROM content
        WHERE language = 'Hindi' AND rating > 8.0 ORDER BY rating DESC
    """)
    print_table(cur, "Q11: Hindi Content with Rating > 8.0")


def main():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    print("Setting up database...")
    conn = setup_database()
    print("Database ready. Running queries...\n")

    run_all_queries(conn)
    conn.close()
    print(f"Database saved to: {DB_FILE}")
    print("You can also open it with: sqlite3 streaming.db")


if __name__ == "__main__":
    main()
