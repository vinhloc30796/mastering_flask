FROM python:3.6.5
# Set the working directory to /app
WORKDIR /app
# Copy local contents into the container
ADD . /app
# Install all required dependencies
RUN pip install -r requirements.txt
ENV FLASK_APP=main.py
EXPOSE 5000
CMD ["python", "main.py"]
