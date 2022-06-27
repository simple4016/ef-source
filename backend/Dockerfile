FROM python:3.6
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
ENV MYSQL_URL=mysql-v2:3306
ENV MYSQL_USERNAME=cff
ENV MYSQL_PASSWORD=cffmysql
ENV CFF_DB=cff-v2
CMD ["sh","-c","pip install --upgrade 'SQLAlchemy<1.4' && python3 api.py"]
