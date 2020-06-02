json=$(jq -r "." ./target.json)
tourl=$(echo ${json} | jq -r ".tourl")
toCometUrl=$(echo ${json} | jq -r ".toCometUrl")
fiwareService=$(echo ${json} | jq -r ".fiwareService")
fiwareServicepath=$(echo ${json} | jq -r ".fiwareServicepath")

json=$(cat ./entity.json)
len=$(echo ${json} | jq length)
for i in $( seq 0 $((${len} - 1)) ); do
row=$(echo ${json} | jq .[${i}])

id=$(echo ${row} | jq -r ".id")
type=$(echo ${row} | jq -r ".type")
lenAttr=$(echo ${row} | jq ".attributes" | jq length)

curl=`cat <<EOS
curl --location --request POST '${tourl}/v2/subscriptions' \
--header 'Fiware-Service: ${fiwareService}' \
--header 'Fiware-Servicepath: ${fiwareServicepath}' \
--header 'Content-Type: application/json' \
--data '{
  "description": "A subscription to notify info about Fiware",
  "subject": {
    "entities": [
      {
        "id": "${id}",
        "type": "${type}"
      }
    ],
    "condition": {
      "attrs": [
EOS`

for j in $( seq 0 $((${lenAttr} - 1)) ); do
curl+=$(echo ${row} | jq .attributes[${j}])
test ${j} != $((${lenAttr} - 1)) && curl+=","
done

curl+=`cat <<EOS
      ]
    }
  },
  "notification": {
    "http": {
      "url": "${toCometUrl}/notify"
    },
    "attrs": [
EOS`

for j in $( seq 0 $((${lenAttr} - 1)) ); do
curl+=$(echo ${row} | jq .attributes[${j}])
test ${j} != $((${lenAttr} - 1)) && curl+=","
done

curl+=`cat <<EOS
    ],
  "attrsFormat": "legacy"
  }
}'
EOS`

eval ${curl}

done