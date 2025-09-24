# Dockerfile para Flask + Streamlit
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install poetry
RUN poetry lock
RUN poetry install --no-root
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
EXPOSE 5000 8501
RUN chmod +x start.sh
CMD ["./start.sh"]
