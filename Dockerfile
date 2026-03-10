FROM python:3.10-slim

WORKDIR /app

# Install system essentials
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (Avoid copying cnn.ipynb or datasets if they are in the same folder)
COPY app.py .
COPY mnist_cnn_model.h5 .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]