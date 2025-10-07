# Use PyTorch CUDA base image (includes Python)
FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install \
    numba \
    tqdm \
    more-itertools \
    tiktoken \
    fastapi \
    uvicorn

# Copy whisper source code
COPY whisper-20250625/ ./whisper-20250625/

# Copy main script
COPY main.py .

# Create audio directory
RUN mkdir -p /app/audio

# Set Python path to use local whisper source
ENV PYTHONPATH="/app/whisper-20250625:$PYTHONPATH"

# Expose port for API
EXPOSE 8000

# Default command - start the API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
