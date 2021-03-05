web: gunicorn discobot:app --timeout 15 --keep-alive 5 --log-level debug
heroku ps:scale web=1 worker=5
heroku config:add PORT=33507