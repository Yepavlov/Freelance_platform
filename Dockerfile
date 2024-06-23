# Use Python 3.11.3 slim image as the base
FROM python:3.11.3-slim

# Update package repositories
RUN apt-get update

# Set up working directory
RUN mkdir -p /freelancer_platform
WORKDIR /freelancer_platform

# Copy source code and requirements
COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
COPY ./commands ./commands

# Install dependencies
RUN pip install --upgrade pip && pip install -r ./requirements.txt

# Create logs directory
RUN mkdir -p /freelancer_platform/LOGS

# Expose port (if necessary)
EXPOSE 8000

CMD ["bash"]