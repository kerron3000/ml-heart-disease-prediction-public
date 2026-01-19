# Minimal, security-patched Python image
FROM python:3.9-slim

# Runtime & security hygiene
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create a non-root user (CRITICAL security best practice)
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Set working directory
WORKDIR /heart-iq

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Install dependencies safely
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code & ML artifacts
COPY . .

# Permissions and drop root privileges
RUN chown -R appuser:appuser /heart-iq
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit securely
ENTRYPOINT ["streamlit", "run", "app1_2.py", "--server.port=8501", "--server.address=0.0.0.0"]
