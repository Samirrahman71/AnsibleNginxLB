FROM python:3.11-alpine
WORKDIR /app

# Create necessary directories
RUN mkdir -p templates static

# Copy application files
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Expose the port
EXPOSE 8000

CMD ["python", "app.py"]
