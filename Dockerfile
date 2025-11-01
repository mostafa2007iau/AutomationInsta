# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend requirements file into the container at /app
COPY backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the container at /app
COPY ./backend .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables (can be overridden)
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

# Run main.py when the container launches
# Use uvicorn to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
