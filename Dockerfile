FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kolkata
ENV NODE_ENV=development
ENV DATABASE_URL="sqlite:///rbac_system.db"
ENV SECRET_KEY="b1e7d8fa444004aea9165bdc74c6dff41d94152d1877b9540985a94750f06891"

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libmagic1 \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    tzdata \
    npm \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire application code
COPY . .

# Copy supervisord configuration file explicitly
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies and build
WORKDIR /app/frontend
RUN npm install && \
    npm install -D tailwindcss postcss autoprefixer && \
    npm install -D @types/node @types/react @types/react-dom typescript

# Setup backend and ensure proper permissions
WORKDIR /app/backend
RUN mkdir -p /app/backend && \
    touch rbac_system.db && \
    chmod 777 rbac_system.db

# Create a non-root user
RUN useradd -m -U app_user && \
    chown -R app_user:app_user /app

# Set working directory back to root
WORKDIR /app

# Expose ports for frontend and backend
EXPOSE 8052 8051

# Switch to non-root user
USER app_user

# Command to start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
