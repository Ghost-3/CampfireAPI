# General

CampfireAPI based on [Campfire web](https://github.com/timas130/campfire-web).

## Install

```bash
pip install Campfire-API
```

## Quickstart

Use it without login:
```python
from campfire_api import CampfireAPI

cf = CampfireAPI()
```

with login:
```python
from campfire_api import LoginCampfireAPI

cf = LoginCampfireAPI(your_login, your_password)
```
