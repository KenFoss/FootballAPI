# FootballAPI
This app is a backend service for serving fantasy football data. I am planning on making tutorial videos based on it.

## Setup
1. Create a PostgreSQL database for this project with:
    ```
    CREATE DATABASE your_database_name
    ```
2. Create and activate virtual environment:
    ```
    $ virtualenv env
    $ source env/bin/activate
    ```
3. Run `create_tables.sql` queries to your database:
    ```
    psql -U your_username -d your_database -a -f create_tables.sql
    ```
4. Set environment variables to give the app access to database info:
    ```
        export FOOTBALL_API_HOST='127.0.0.1'
        export FOOTBALL_API_PORT='your_port'
        export FOOTBALL_API_USER='your_user'
        export FOOTBALL_API_PASSWORD='your_pass'
        export FOOTBALL_API_NAME='your_databse_name'
    ```
5. Set the port to run the app on if desired, else it will default to 8000:
    ```
    export FOOTBALL_API_PORT=your_port
    ```
6. Run the app
    `python3 src/football_api_app.py`
    
7. Test the endpoint with postman (add):
    - endpoint: `http://127.0.0.1:8000/api/add_passing_data`
    - data: 
        ```
        {   
            "player_id" : 1,
            "player_name" : "Tom Brady",
            "year" : 2022,
            "interceptions" : 2,
            "touchdowns" : 70,
            "ypa" : 7.0,
            "attempts" : 600
        }
        ```
8. Test the endpoint with postman (update):
    - endpoint: `http://127.0.0.1:8000/api/add_passing_data`
    - data: 
      ```
        {   
            "player_id" : 1,
            "player_name" : "Tom Brady",
            "year" : 2022,
            "interceptions" : 3
        }
      ```