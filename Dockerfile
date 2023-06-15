# start by pulling the python image
FROM python:3.8-alpine
# copy the requirements file into the image
# switch working directory
WORKDIR /amo_auth
COPY . /amo_auth
# install the dependencies and packages in the requirements file
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy every content from the local file to the image
# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["main.py"]