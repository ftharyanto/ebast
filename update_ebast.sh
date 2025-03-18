mv db.sqlite3 ..
git pull
mv ../db.sqlite3 .
python manage.py makemigrations && python manage.py migrate
sudo systemctl restart ebast.service