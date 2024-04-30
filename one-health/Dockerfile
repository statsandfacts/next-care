# Set environment variables
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    mysql-client \
    libmysqlclient-dev \
    gcc

# Install Python packages with mysqlclient and specify include directory
RUN pip3 install --no-cache-dir --global-option=build_ext --global-option="-I/usr/include/mysql" mysqlclient

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application directory into the container
COPY . .

# Run the FastAPI application with Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]