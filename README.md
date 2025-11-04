MAKE SURE YOU HAVE DOCKER INSTALLED AND RUNNING
"https://www.docker.com/products/docker-desktop/"

To run the app go to the terminal and write "docker-compose up"
then go to "http://localhost:5001/register"

To view users table in Dockerized PostgreSQL database
make sure you build it first with docker-compose up --build that will launch the app running with docker
when running after that you can just use docker-compose up
then in another terminal run
"docker exec -it groupproject-db-1 psql -U postgres -d ics499db"
then in that same terminal run "SELECT \* FROM users"

IF YOUR CONTAINER NAME IS DIFFERENT SWAP "groupproject" with whatever your container is called

to exit do Ctrl + C or press enter in the first terminal that runs the app.
