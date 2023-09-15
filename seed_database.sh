rm db.sqlite3
rm -rf ./shutterbugapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations shutterbugapi
python3 manage.py migrate shutterbugapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata shutterbug_users
python3 manage.py loaddata categories
python3 manage.py loaddata posts
python3 manage.py loaddata tags
python3 manage.py loaddata post_tags
python3 manage.py loaddata reactions
python3 manage.py loaddata post_reactions
python3 manage.py loaddata comments
python3 manage.py loaddata direct_messages

