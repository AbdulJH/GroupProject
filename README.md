MAKE SURE YOU HAVE DOCKER INSTALLED AND RUNNING
"https://www.docker.com/products/docker-desktop/"

To run the app go to the terminal and write "docker-compose up"
then go to "http://localhost:5001/register"

To view users table in Dockerized PostgreSQL database
make sure dockers is running first with the docker-compose up
then in another terminal run
"docker exec -it ics499-db-1 psql -U postgres -d ics499db"
then in that same terminal run "SELECT \* FROM users"

to exit do Ctrl + C in the first terminal that runs the app.
