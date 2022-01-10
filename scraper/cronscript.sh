cd /home/skunz1/reddit-map/scraper
python3 scraper.py ../creds.txt
git add ../json/all.geojson
git commit -m "daily endpoint update"
git push origin main
