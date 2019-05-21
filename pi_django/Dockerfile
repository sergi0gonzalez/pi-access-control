FROM python:3.6.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /music_service

# Set the working directory to /music_service
WORKDIR /pi_django

# Copy the current directory contents into the container at /music_service
ADD . /pi_django

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000