#!/bin/bash
### jqのインストール後に動作させることを想定しています
# 引数が3個以上の時はエラーにする
if [ $# -gt 2 ]; then
echo "引数は2個以下にしてください"
return
fi
# 引数が2個の時
if [ $# -eq 2 ]; then
fromdate=$(date -d $1 '+%Y-%m-%dT%H:%M:%SZ')
todate=$(date -d $2 '+%Y-%m-%dT%H:%M:%SZ')

# 引数が1個の時は取得開始日時を設定する
elif [ $# -eq 1 ]; then
fromdate=$(date -d $1 '+%Y-%m-%dT%H:%M:%SZ')
# 現在時刻を取る
todate=$(date '+%Y-%m-%dT%H:%M:%SZ')
echo ${todate} > ./.history

# 引数が0個の時は前回の起動時間～現在時刻までのデータを設定する
else
# 前回の起動時刻を取る
fromdate=""
if [[ -f ./.history ]]; then
DATA=`cat ./.history`
while read list
do
fromdate=$list
done << FILE
$DATA
FILE
fi
if [ "${fromdate}" == "" ]; then
fromdate="2000-01-01T00:00:00Z"
fi
# 現在時刻を取る
todate=$(date '+%Y-%m-%dT%H:%M:%SZ')
echo ${todate} > ./.history
fi

# 日付型に変換できない時はエラーで終了する
if [ "${fromdate}" == "" ]; then
echo "引数は日付を入力してください"
return
elif [ "${todate}" == "" ]; then
echo "引数は日付を入力してください"
return
fi

json=$(jq -r "." ./target.json)
fromurl=$(echo ${json} | jq -r ".fromurl")
tourl=$(echo ${json} | jq -r ".tourl")
fiwareService=$(echo ${json} | jq -r ".fiwareService")
fiwareServicepath=$(echo ${json} | jq -r ".fiwareServicepath")

json=$(cat ./entity.json)
len=$(echo ${json} | jq length)
for i in $( seq 0 $((${len} - 1)) ); do
row=$(echo ${json} | jq .[${i}])

id=$(echo ${row} | jq -r ".id")
type=$(echo ${row} | jq -r ".type")
lenAttr=$(echo ${row} | jq ".attributes" | jq length)
for j in $( seq 0 $((${lenAttr} - 1)) ); do
attribute=$(echo ${row} | jq -r .attributes[${j}])
curl=`cat <<EOS
curl --location --request GET '${fromurl}/STH/v1/contextEntities/type/${type}/id/${id}/attributes/${attribute}?lastN=100&dateFrom=${fromdate}&dateTo=${todate}' \
--header 'fiware-service: ${fiwareService}' \
--header 'fiware-servicepath: ${fiwareServicepath}'
EOS`
echo ${curl}
JSON_RESPONSE=$(eval ${curl})

name=$(echo $JSON_RESPONSE | jq -r ".contextResponses[].contextElement.attributes[].name")
value=$(echo $JSON_RESPONSE | jq ".contextResponses[].contextElement.attributes[].values")
lenValue=$(echo ${value} | jq length)
for k in $( seq 0 $((${lenValue} - 1)) ); do
putcurl=`cat <<EOS
curl --location --request PATCH '${tourl}/v2/entities/${id}/attrs' \
--header 'Fiware-Service: dbs' \
--header 'Fiware-Servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "${name}": {
      "value": $(echo ${value} | jq -r .[${k}].attrValue), 
      "type": "$(echo ${value} | jq -r .[${k}].attrType)",
      "metadata": {
          "TimeInstant": {
              "value": "$(echo ${value} | jq -r .[${k}].recvTime)",
              "type": "ISO8601"
          }
        }
    }
}'
EOS`
echo ${putcurl}
eval ${putcurl}
done

done

done
