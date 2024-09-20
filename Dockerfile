FROM python:3.12.6-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/bin/bash"]