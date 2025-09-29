#!/bin/sh
poetry run python api/main.py &
poetry run streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 &
wait

