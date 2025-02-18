FROM python:3.9

WORKDIR /src

COPY requirements.txt .
COPY ./src ./src
COPY src/.env src/.env

#RUN pip install uv
#RUN uv venv
#RUN source .venv/bin/activate
#RUN uv pip compile requirements.in -o requirements.txt
#RUN uv pip sync requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#pip install --no-cache-dir -r requirements.txt
#uv pip compile requirements.in -o requirements.txt 

CMD ["python", "./src/main.py"]