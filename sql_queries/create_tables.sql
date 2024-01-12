CREATE TABLE IF NOT EXISTS passing_stats (
    player_id INT,
    player VARCHAR(50),
    team_name VARCHAR(50),
    year INT,
    interceptions INT,
    touchdowns INT,
    ypa FLOAT,
    attempts INT
    PRIMARY KEY (player_id, year)
);

CREATE TABLE IF NOT EXISTS rushing_stats (
    player_id INT,
    player VARCHAR(50),
    team_name VARCHAR(50),
    year INT,
    attempts INT,
    targets INT,
    receptions INT,
    touchdowns INT,
    ypa FLOAT
    PRIMARY KEY (player_id, year)
)

CREATE TABLE IF NOT EXISTS receiving_stats (
    player_id INT,
    player VARCHAR(50),
    team_name VARCHAR(50),
    year INT,
    caught_percent FLOAT,
    drop_rate FLOAT,
    receptions INT,
    targets INT,
    touchdowns INT
    PRIMARY KEY (player_id, year)
)