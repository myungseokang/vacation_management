
휴가관리 웹사이트
===

[![Build Status](https://travis-ci.org/Leop0ld/vacation_management.svg?branch=master)](https://travis-ci.org/Leop0ld/vacation_management)

### 기술스택
 - Python 3.6 & Django 2.0
 - jQuery 3.x
 - Semantic


### 실행방법

```
$ git clone https://github.com/Leop0ld/vacation_management.git
$ pip install -r requirements/local.txt
$ pip install -r requirements/test.txt
$ python manage.py migrate  # Need a PostgreSQL database "vacation"
$ python manage.py createsuperuser
$ python manage.py runserver
```

### 테스트 실행하기

```
$ pip install -r requirements/test.txt
$ pytest
```
