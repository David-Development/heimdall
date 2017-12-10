cd upload

for f in resized/*.jpg
do
 echo "Recognizing $f"
 #(echo '{ "image": "'; base64 "$f"; echo '"}') | curl -H 'cache-control: no-cache' -H 'content-type: application/json' -X POST -d @-  http://192.168.10.38:5000/api/live/
 (echo '{ "image": "'; base64 "$f"; echo '"}') | curl -H 'cache-control: no-cache' -H 'content-type: application/json' -X POST -d @-  http://localhost:5000/api/live/
 sleep 5
done;