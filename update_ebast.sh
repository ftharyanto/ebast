mv db.sqlite3 ..
git pull
mv ../db.sqlite3 .
dmigrate
sudo systemctl restart ebast.service