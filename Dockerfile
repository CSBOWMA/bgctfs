FROM python:3.13.0-bookworm

WORKDIR /challenges
COPY . /challenges

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "/challenges/setup-challenges.sh" ]
