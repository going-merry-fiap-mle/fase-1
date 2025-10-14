#!/bin/sh
poetry run streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0

