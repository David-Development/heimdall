cd upload
mkdir resized
rm resized/*

for i in *.png
do 
    sips -s format jpeg -s formatOptions 70 "${i}" --out "${i%png}jpg";
    rm "$i"
done;

for f in *.jpg
do
    resizedFilename="resized/$f"
    cp "$f" "$resizedFilename"
    sips -Z 640 "$resizedFilename"
    #sips -z 400 640 $resizedFilename
done;
#for f in *.jpg
#do
# b64fname="$f.base64"
# echo "Processing $f --> $b64fname"
# base64 -i $f -o $b64fname
#done;

#for f in *.base64
for f in resized/*.jpg
do
 echo "Uploading $f"
 (echo '{ "image": "'; base64 "$f"; echo '"}') | curl -H 'cache-control: no-cache' -H 'content-type: application/json' -X POST -d @-  http://localhost:5000/api/image/upload/
done;