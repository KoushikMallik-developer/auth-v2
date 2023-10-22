
# AUTH
![](https://img.shields.io/badge/Python-3.11-green.svg)





An API layer to authenticate users and update profile details.

Your README file is normally the first entry point to your code. It should tell people why they should use your module, how they can install it, and how they can use it. Standardizing how you write your README makes creating and maintaining your READMEs easier. Great documentation takes work!

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)


## Installation

Clone the Git repository `auth`

`https://github.com/KoushikMallik-developer/auth-v2.git`

Create your virtual-environment for `auth` outside of the project root directory.

```bash
  python -m venv auth-env
  cd auth-env
  .\auth-env\Scripts\activate
```
Activate the environment.

```bash
  .\auth-env\Scripts\activate
```
Now install all the dependencies in auth-env.

```bash
  pip install -r .\dependencies\dev-requirements.txt
```
Go to project directory.

```bash
  cd auth
```

Rename the file `test.env` to `.env`

Run the below commands to make the migrations for database models.

```bash
  python .\manage.py makemigrations
  python .\manage.py migrate
```

Run the server.

```bash
  python .\manage.py runserver 8080
```
