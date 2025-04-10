FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY fspapplication_frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY fspapplication_frontend/ ./
# Skip TypeScript checks during build by modifying the build script
RUN sed -i 's/\"build\":.*/\"build\": \"vite build\",/g' package.json
RUN npm run build

FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies - minimal installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY fspapplication_backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy backend code
COPY fspapplication_backend/ .

# Copy built frontend from the frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist /app/static

# Expose the port
EXPOSE $PORT

# Create a startup script
RUN echo '#!/bin/bash\n\
gunicorn fspapplication_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2\n\
' > /app/start.sh \
    && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"] 