FROM python:3.7

RUN echo LANG="en_US.UTF-8" > /etc/default/locale
RUN echo LANGUAGE="en_US" > /etc/default/locale
RUN echo LC_ALL="en_US.UTF-8" > /etc/default/locale

RUN pip install pipenv
ENV PROJECT_DIR /app
WORKDIR ${PROJECT_DIR}
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy
COPY . /app