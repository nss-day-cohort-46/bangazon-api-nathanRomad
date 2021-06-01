"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import 
from bangazonreports.views import Connection


def favseller_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    c.id custId,
                    u.first_name || ' ' || u.last_name AS fullName,
                    u.username,
                    fav.id favId
                FROM
                    bangazonapi_customer c
                JOIN
                    bangazonapi_favorite fav ON c.id = fav.customer_id
                JOIN
                    auth_user u ON c.id = u.id
            """)

            dataset = db_cursor.fetchall()

            games_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                game = Game()
                game.title = row["title"]
                game.maker = row["maker"]
                game.skill_level = row["skill_level"]
                game.number_of_players = row["number_of_players"]
                game.gametype_id = row["gametype_id"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in games_by_user:

                    # Add the current game to the `games` list for it
                    games_by_user[uid]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_games = games_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_games.html'
        context = {
            'usergame_list': list_of_users_with_games
        }

        return render(request, template, context)