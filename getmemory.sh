#!/bin/bash
#
THRESHOLD=80
ADDRESS="http:/localhost:8082"
FILE_WITH_ID="_id"
INTERVAL=60

make_request(){
    MAX_MEM=$1
    USED_MEM=$2
    PERCENT=$3
    MESSAGE='{"status": {"hostname": "'$(hostname)'", "used_memory": '$USED_MEM', "max_memory": '$MAX_MEM', "limit": '$PERCENT'}}'
    $(curl -X POST -H "Content-Type: application/json" -d "$MESSAGE" "$ADDRESS" >>  $FILE_WITH_ID )
}
while true; do
# Get maximum memory and used memory
    MESSAGE=$(free -m | awk 'NR==2 { print $2, $4}' FS=' ' OFS=' ' )
    MAXIMUM_MEMORY=$(echo $MESSAGE | awk '{print $1}')
    USED_MEMORY=$(echo $MESSAGE | awk '{print $2}')

# Calculate value
    PERCENTAGE=$(awk "BEGIN {printf \"%.1f\n\", 100*$USED_MEMORY/$MAXIMUM_MEMORY}")
    LEVEL=$(echo $PERCENTAGE |  sed -r "s/(.[0-9]+)$//")

# If the threshold is exceeded it sends message
    if [[ $LEVEL -gt  $THRESHOLD ]]; then
        make_request $MAXIMUM_MEMORY $USED_MEMORY $PERCENTAGE
    fi
    sleep $INTERVAL
done
