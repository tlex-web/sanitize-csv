# base image
FROM python:alpine

# create working directory
WORKDIR /app

# copy the requirements into the image
COPY requirements.txt requirements.txt

# install the requirements
RUN pip3 install -r requirements.txt

# copy source code into the image
COPY . .

# run the application
CMD [ "python", "-m" , "sanitize_csv"]
