# roop forever
count=0
while true ; do
    echo "count: $count"
  ./battlesnake.exe play -W 6 -H 6 --name 'PBL 7' --url http://localhost:$1 -g solo --browser --foodSpawnChance 0 --minimumFood 3
    count=$((count+1))
done