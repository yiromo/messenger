FROM python:3.9

WORKDIR /src

COPY requirements.txt .
COPY ./src ./src

#RUN pip install uv
RUN pip install --no-cache-dir -r requirements.txt

#pip install --no-cache-dir -r requirements.txt
#uv pip compile requirements.in -o requirements.txt 

CMD ["python", "./src/main.py"]