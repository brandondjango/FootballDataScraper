# Use an official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome's official repository to the sources list
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Clone the PyAI Git repository
RUN git clone https://github.com/brandondjango/PyAI.git /PyAI

# Set the working directory to the project root
WORKDIR /PyAI

RUN mkdir -p /PyAI/drivers

# Download ChromeDriver and move it to the drivers directory
RUN CHROMEDRIVER_VERSION=128.0.6613.84 \
    && wget -q https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip -d /tmp/chromedriver
RUN mv /tmp/chromedriver/chromedriver-linux64/chromedriver /PyAI/drivers/chromedriver
RUN rm -rf /tmp/chromedriver chrome-linux64.zip

# Optionally, install Python dependencies (if required by the PyAI project)
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Set the entrypoint to bash
CMD ["python", "main.py"]