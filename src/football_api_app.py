# from flask import Flask, request, jsonify
# import flask
from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import os
import traceback

app = Flask(__name__)


# Connection to PostgreSQL db, using os variables to not expose sensative server information on github
conn = psycopg2.connect(
    host = os.environ.get('FOOTBALL_API_HOST', '127.0.0.1'),    
    port = os.environ.get('FOOTBALL_API_PORT',  '5432'),    
    user = os.environ.get('FOOTBALL_API_USER',  'kfoss'),    
    password = os.environ.get('FOOTBALL_API_PASSWORD',  ''),    
    database = os.environ.get('FOOTBALL_API_NAME',  'footballapi') 
)
cursor = conn.cursor()

app = Flask(__name__)

@app.route('/api/add_passing_data', methods=['POST'])
def add_passing_data():
    try:
        #get data from request body
        data = request.get_json()

        # Get the player id, if there is none passed this will raise
        # a value error that is caught below
        player_id = data.get('player_id')
        year = data.get('year')
        # print(data)

        # Query table to see if player data exists
        # This table has a primary key on the player_id and year
        # So, queries on these values are faster
        player_exists_query = sql.SQL('SELECT 1 FROM passing_stats WHERE player_id = %s AND year = %s;')
        cursor.execute(player_exists_query, (player_id, year,))
        player_exists = cursor.fetchall()

        if player_exists:
            # The player exists so this request is to update their stats for given year

            # Filter out unwanted keys, eliminate sql injection risk
            data = dict(filter( 
                    lambda x: x[0] == 'interceptions' or x[0] == 'touchdowns' or  x[0] == 'player' or
                                x[0] == 'ypa' or x[0] == 'attempts' or x[0] == 'team_name' 
                    ,data.items()))
            
            # Build a query dynamically based on passed data, this is not recommended unless
            #   you ensure the data is exactly what you expect to avoid an injection risk (we did this above)     
            set_clause = ', '.join(f'{column} = %s' for column,value in data.items())
            print(f'Set Clause Is: {set_clause}')
            print(f'data is: {data}')
            # print(f'testing {dict(filter(lambda x:))}')
            update_passing_stats_query = f'UPDATE passing_stats SET {set_clause} WHERE player_id = %s AND year = %s RETURNING *;'

            values = [value for value in data.values()]
            values.append(player_id)
            values.append(year)

            # Make a tuple from values to properly execute this query
            cursor.execute(update_passing_stats_query, tuple(values))
            updated_data = cursor.fetchall()
            conn.commit()

            # Return updated data and ok status
            #     On the calling end when returned status is bnetween 200 and 299 inclusive
            #     response.ok will return TRUE
            return jsonify({'data' : updated_data}), 200
        else:
            # This player does not have stats for given year, insert them into the table
            player = data.get('player') 
            team_name = data.get('team_name')
            # Without default values... errors are thrown when player name and team name not given

            interceptions = data.get('interceptions', 0)
            touchdowns = data.get('touchdowns', 0)
            yards_per_attempt = data.get('ypa', 0.0)
            attempts = data.get('attempts', 0)

            insert_passing_stats_query = 'INSERT INTO passing_stats (player_id, player, team_name, year, interceptions, touchdowns, ypa, attempts) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *'
            
            cursor.execute(insert_passing_stats_query, \
                (player_id, player, team_name, year, interceptions, touchdowns, yards_per_attempt, attempts, ))
            inserted_data = cursor.fetchall()
            conn.commit()

            return jsonify({'data' : inserted_data}), 200
        
    except ValueError as ve:
        # Throw a bad request if we hit a value error when required data is not passed
        error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({'error' : str(ve)}), 400 
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(port=os.environ.get('FOOTBALL_API_PORT', 8000), debug=True)