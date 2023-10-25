FROM python:3.9.18-alpine3.18

	
WORKDIR /app
COPY server .
COPY requirements requirements
RUN	pip install -r requirements
# ENV FLASK_RUN_HOST=0.0.0.0
CMD [ "python3", "/app/server.py" ]

EXPOSE 8080
