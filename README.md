MusixCue
========

Basic Deployment
----------------
1. Create a Python virtual environment and use Python3.6

2. Put the 'settings.ini' in 'DBproject' directory

3. Install necessary module
   ```
    $ pip install -r requirements.txt
   ```

4. Run server in localhost
   ```
    $ python manage.py runserver
   ```

## Instructions of using docker to launch DB
```bash
docker run -p 3306:3306 --name musixcue-mysql -e MYSQL_ROOT_PASSWORD=123 -e MYSQL_DATABASE=musixcue -d mysql:5.7
```
```bash
cat << EOF > DBproject/settings.ini
[settings]
NAME=musixcue
USER=root
PASSWORD=123
HOST=127.0.0.1
EOF
```
