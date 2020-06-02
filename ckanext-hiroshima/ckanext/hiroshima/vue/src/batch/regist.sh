json=$(jq -r "." target.json)
tourl=$(echo ${json} | jq -r ".tourl")
fiwareService=$(echo ${json} | jq -r ".fiwareService")
fiwareServicepath=$(echo ${json} | jq -r ".fiwareServicepath")

json=$(cat entity.json)
len=$(echo ${json} | jq length)
for i in $( seq 0 $((${len} - 1)) ); do
row=$(echo ${json} | jq .[${i}])

id=$(echo ${row} | jq -r ".id")
type=$(echo ${row} | jq -r ".type")
lenAttr=$(echo ${row} | jq ".attributes" | jq length)

curl=`cat <<EOS
curl --location --request POST '${tourl}/v2/entities' \
--header 'Fiware-Service: ${fiwareService}' \
--header 'Fiware-Servicepath: ${fiwareServicepath}' \
--header 'Content-Type: application/json' \
--data '{
  "id": "${id}",
  "type": "${type}",
EOS`

for j in $( seq 0 $((${lenAttr} - 1)) ); do
curl+=$(echo ${row} | jq .attributes[${j}])
curl+=':{ "value":'
curl+=$(echo ${row} | jq -r .attributesDate[${j}].Default)
curl+=', "type":'
curl+=$(echo ${row} | jq .attributesDate[${j}].Type)
curl+=', "metadata": { "TimeInstant": { "value": "2000-01-01T00:00:00Z", "type": "ISO8601" }}}'
test ${j} != $((${lenAttr} - 1)) && curl+=","
done

curl+=`cat <<EOS
}'
EOS`

eval ${curl}

done