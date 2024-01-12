import psycopg2
import os
# import cursor

# Replace these with your PostgreSQL connection details
connection_params = {
    'host': '127.0.0.1',
    'database': 'footballapi',
    'user': 'kfoss',
    'password': '1234',
}

tables = [ 
    '''
        CREATE TABLE IF NOT EXISTS passing_stats (
            player_id INT,
            player VARCHAR(50),
            team_name VARCHAR(50),
            year INT,
            interceptions INT,
            touchdowns INT,
            ypa FLOAT,
            attempts INT,
            PRIMARY KEY (player_id, year)
        );
    ''',
    '''
        CREATE TABLE IF NOT EXISTS rushing_stats (
            player_id INT,
            player VARCHAR(50),
            team_name VARCHAR(50),
            year INT,
            attempts INT,
            targets INT,
            receptions INT,
            touchdowns INT,
            ypa FLOAT,
            PRIMARY KEY (player_id, year)
        );
    ''', 
    '''
        CREATE TABLE IF NOT EXISTS receiving_stats (
            player_id INT,
            player VARCHAR(50),
            team_name VARCHAR(50),
            year INT,
            caught_percent FLOAT,
            drop_rate FLOAT,
            receptions INT,
            targets INT,
            touchdowns INT,
            PRIMARY KEY (player_id, year)
        )
    '''
]

sql_script_dir = f'{os.path.dirname(os.path.abspath(__file__))}/sql_queries/create_tables.sql'

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()

    # Read and execute the SQL script
    for table in tables:
        cursor.execute(table)

    # Commit the changes
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

except Exception as e:
    print(f"Error: {e}")

