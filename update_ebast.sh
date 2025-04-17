mv db.sqlite3 ..
git pull
mv ../db.sqlite3 .
python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput
sudo systemctl restart ebast.service