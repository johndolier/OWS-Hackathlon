

# check if script is started with '-b' flag
if [ "$1" == "-b" ]; then
    # build docker image
    docker build -t ows-hackathlon-backend .
fi

docker run -p 80:80 ows-hackathlon-backend

