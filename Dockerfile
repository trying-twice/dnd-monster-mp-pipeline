# Use the official Prefect image as the base
FROM prefecthq/prefect:2-latest

# Set the working directory
WORKDIR /app

# Copy your requirements file
COPY requirements.txt .

# Install your Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your flow code
COPY src/ . 