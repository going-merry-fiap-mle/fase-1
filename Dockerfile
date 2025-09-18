# Dockerfile para Flask + Streamlit
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install poetry && poetry install --no-root
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"
EXPOSE 5000 8501
CMD ["sh", "-c", "poetry run streamlit run frontend/app.py & poetry run python api/main.py"]
