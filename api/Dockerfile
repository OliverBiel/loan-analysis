FROM python:3.10.3-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN sed -i -e 's/\r$//' entrypoint.sh && \
    chmod +x entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]