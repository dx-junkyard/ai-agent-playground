CREATE TABLE browsing_logs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    url TEXT,
    title TEXT,
    body_text LONGTEXT,
    scroll_depth FLOAT,
    visit_start DATETIME,
    visit_end DATETIME,
    keywords TEXT,
    search_query TEXT,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
