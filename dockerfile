# specify start image
FROM python

# all commands start from this directory
WORKDIR /klipper-mailbot

# copy all files from this folder to working directory (ignores files in .dockerignore)
COPY . .

# install all packages needed
RUN pip install requests

# set the start command
CMD [ "python","-u","main.py" ]

#after use <docker build -t godaddy-dyndns .> and <docker run godaddy-dyndns>