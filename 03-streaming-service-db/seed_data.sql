-- ============================================================
-- Seed Data — populate the streaming service database
-- ============================================================

-- Users
INSERT INTO users (name, email, country, plan) VALUES
('Arjun Sharma',    'arjun@example.com',   'India', 'premium'),
('Priya Mehta',     'priya@example.com',   'India', 'standard'),
('Rahul Verma',     'rahul@example.com',   'India', 'basic'),
('Sneha Patel',     'sneha@example.com',   'India', 'premium'),
('Amit Kumar',      'amit@example.com',    'India', 'free'),
('Divya Nair',      'divya@example.com',   'India', 'standard'),
('Kiran Reddy',     'kiran@example.com',   'India', 'premium'),
('Anjali Singh',    'anjali@example.com',  'India', 'basic'),
('Rohit Gupta',     'rohit@example.com',   'India', 'standard'),
('Meera Iyer',      'meera@example.com',   'India', 'premium');

-- Content
INSERT INTO content (title, type, genre, language, release_year, rating, duration_min, description) VALUES
('Sacred Games',         'series',      'Crime/Thriller',  'Hindi',   2018, 8.8, NULL,  'A police officer uncovers a web of crime in Mumbai.'),
('3 Idiots',             'movie',       'Comedy/Drama',    'Hindi',   2009, 8.4, 170,   'Three friends navigate engineering college life.'),
('Mirzapur',             'series',      'Crime/Drama',     'Hindi',   2018, 8.5, NULL,  'Power, crime and chaos in Uttar Pradesh.'),
('Dangal',               'movie',       'Sports/Drama',    'Hindi',   2016, 8.4, 161,   'A father trains his daughters to become wrestlers.'),
('Panchayat',            'series',      'Comedy/Drama',    'Hindi',   2020, 8.8, NULL,  'A city graduate works as a panchayat secretary.'),
('RRR',                  'movie',       'Action/Drama',    'Telugu',  2022, 7.9, 187,   'Two legendary revolutionaries fight British rule.'),
('Scam 1992',            'series',      'Finance/Drama',   'Hindi',   2020, 9.3, NULL,  'The rise and fall of stockbroker Harshad Mehta.'),
('Bajrangi Bhaijaan',    'movie',       'Drama',           'Hindi',   2015, 8.0, 163,   'A man helps a mute Pakistani girl return home.'),
('Delhi Crime',          'series',      'Crime/Drama',     'Hindi',   2019, 8.5, NULL,  'Investigation of the 2012 Delhi gang rape case.'),
('PK',                   'movie',       'Comedy/Drama',    'Hindi',   2014, 8.1, 153,   'An alien questions religious practices in India.'),
('Breathe',              'series',      'Thriller',        'Hindi',   2018, 7.5, NULL,  'A man breaks the law to save his dying son.'),
('Queen',                'movie',       'Drama',           'Hindi',   2014, 8.1, 146,   'A woman goes on her honeymoon alone after breakup.'),
('Masaan',               'movie',       'Drama',           'Hindi',   2015, 8.0, 110,   'Four lives intersect on the Ganges in Varanasi.'),
('Paatal Lok',           'series',      'Crime/Thriller',  'Hindi',   2020, 8.1, NULL,  'A police inspector investigates a complex murder plot.'),
('Drishyam 2',           'movie',       'Thriller',        'Hindi',   2022, 8.3, 152,   'A man struggles to protect his family from the truth.');

-- Episodes (for Sacred Games S1)
INSERT INTO episodes (content_id, season, episode_num, title, duration_min) VALUES
(1, 1, 1, 'Ashwathama',     53),
(1, 1, 2, 'Halahala',       48),
(1, 1, 3, 'Aatapi Vatapi',  50),
(1, 1, 4, 'Brahmahatya',    52),
(1, 1, 5, 'Sarama',         49),
(1, 1, 6, 'Pretakalpa',     55),
(1, 1, 7, 'Rudra',          54),
(1, 1, 8, 'Yayati',         57);

-- Watch History
INSERT INTO watch_history (user_id, content_id, percent_watched, completed) VALUES
(1, 1,  100, 1), (1, 2,  100, 1), (1, 3,  85,  0), (1, 7,  100, 1),
(2, 2,  100, 1), (2, 4,  100, 1), (2, 5,  60,  0), (2, 6,  100, 1),
(3, 3,  100, 1), (3, 6,  100, 1), (3, 8,  75,  0),
(4, 1,  100, 1), (4, 5,  100, 1), (4, 7,  100, 1), (4, 9,  100, 1),
(5, 2,  40,  0), (5, 10, 100, 1),
(6, 7,  100, 1), (6, 9,  80,  0), (6, 12, 100, 1),
(7, 1,  100, 1), (7, 3,  100, 1), (7, 7,  100, 1), (7, 14, 90,  0),
(8, 4,  100, 1), (8, 6,  100, 1), (8, 8,  100, 1),
(9, 2,  100, 1), (9, 5,  100, 1), (9, 15, 100, 1),
(10,7,  100, 1), (10,9,  100, 1), (10,14, 100, 1);

-- Ratings
INSERT INTO ratings (user_id, content_id, stars, review) VALUES
(1, 1, 5, 'Brilliant storytelling!'),
(1, 2, 5, 'All-time favourite movie.'),
(1, 7, 5, 'Best Indian web series ever.'),
(2, 2, 5, 'Masterpiece of Indian cinema.'),
(2, 4, 4, 'Inspiring story, great performances.'),
(2, 6, 5, 'Visually stunning and epic!'),
(3, 3, 4, 'Gripping and dark.'),
(3, 6, 5, 'RRR is absolutely phenomenal.'),
(4, 7, 5, 'Scam 1992 changed how I see finance.'),
(4, 5, 5, 'So heartwarming and funny.'),
(5, 10, 4, 'Makes you think about religion differently.'),
(6, 7, 5, 'A masterclass in storytelling.'),
(7, 1, 5, 'Kept me up all night.'),
(7, 3, 4, 'Raw and intense.'),
(8, 4, 5, 'Aamir Khan at his best.'),
(9, 2, 5, 'Watched it 3 times already!'),
(10,7, 5, 'No words. Just watch it.');

-- Watchlist
INSERT INTO watchlist (user_id, content_id) VALUES
(1, 5), (1, 9), (1, 14),
(2, 3), (2, 7),
(3, 1), (3, 5),
(4, 6), (4, 10),
(5, 1), (5, 3), (5, 7),
(6, 4), (6, 5),
(7, 4), (7, 8),
(8, 1), (8, 5), (8, 7),
(9, 3), (9, 7),
(10, 2), (10, 5);

-- Tags
INSERT INTO tags (name) VALUES
('Action'), ('Comedy'), ('Drama'), ('Thriller'), ('Crime'),
('Sports'), ('Finance'), ('Romance'), ('Mystery'), ('Family');

-- Content Tags
INSERT INTO content_tags (content_id, tag_id) VALUES
(1,  4), (1,  5),   -- Sacred Games: Thriller, Crime
(2,  2), (2,  3),   -- 3 Idiots: Comedy, Drama
(3,  5), (3,  3),   -- Mirzapur: Crime, Drama
(4,  6), (4,  3),   -- Dangal: Sports, Drama
(5,  2), (5,  3),   -- Panchayat: Comedy, Drama
(6,  1), (6,  3),   -- RRR: Action, Drama
(7,  7), (7,  3),   -- Scam 1992: Finance, Drama
(8,  3), (8, 10),   -- Bajrangi Bhaijaan: Drama, Family
(9,  5), (9,  4),   -- Delhi Crime: Crime, Thriller
(10, 2), (10, 3),   -- PK: Comedy, Drama
(11, 4),            -- Breathe: Thriller
(12, 3), (12, 8),   -- Queen: Drama, Romance
(13, 3),            -- Masaan: Drama
(14, 5), (14, 4),   -- Paatal Lok: Crime, Thriller
(15, 4), (15, 9);   -- Drishyam 2: Thriller, Mystery
