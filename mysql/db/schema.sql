CREATE TABLE IF NOT EXISTS browsing_logs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    url TEXT,
    title TEXT,
    summary TEXT,
    scroll_depth FLOAT,
    visit_start DATETIME,
    visit_end DATETIME,
    keywords TEXT,
    search_query TEXT,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS root_categories (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS sub_categories (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    root_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (root_id) REFERENCES root_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS log_sub_categories (
    log_id BIGINT UNSIGNED NOT NULL,
    sub_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (log_id, sub_id),
    FOREIGN KEY (log_id) REFERENCES browsing_logs(id),
    FOREIGN KEY (sub_id) REFERENCES sub_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
