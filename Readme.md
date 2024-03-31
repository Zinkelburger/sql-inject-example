# SQL Injection Example
Some simple sql injections for the UML Cyber Security Club. Uses Django. Only important bits are that the webpages/database queries are defined in `vulnerable_app/views.py`, and the postgres database is defined in the docker compose file.

Feel free to add more examples/memes.

## Deployment
`git clone https://github.com/Zinkelburger/sql-inject-example.git`

`docker-compose up --build`

Navigate to `0.0.0.0:8000/admin1`, `admin2`, etc. Try to sql inject these pages.
