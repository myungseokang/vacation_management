휴가관리 웹사이트
===

[![Build Status](https://travis-ci.org/Leop0ld/vacation_management.svg?branch=master)](https://travis-ci.org/Leop0ld/vacation_management)

### 기술스택
 - Python 3.6 & Django 1.11
 - jQuery 3.x
 - Semantic


### 실행방법


```
# Run
$ docker-compose up
```


```
# Re-build
$ docker-compose up --build
```

```
# create superuser
$ docker-compose -f docker-compose.yml run django python manage.py createsuperuser
```