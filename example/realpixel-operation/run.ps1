docker ps -a -q | % { docker rm $_ }
docker images | ConvertFrom-String | where {$_.P2 -eq "<none>"} | % { docker rmi $_.P3 }

$GTDS_DEFINITIONS = [IO.File]::ReadAllText("example/realpixel-operation/definitions.yaml")

## build 
docker build --build-arg DEFINITIONS="$GTDS_DEFINITIONS" --build-arg VERSION=0.1.0 --build-arg SERVER_HOST=localhost --build-arg SERVER_PORT=8888 --build-arg SERVRE_BASE_PATH=v1 -t gtds-realpixel-operation:0.1.0 ../../
 
## run locally
docker-compose -p realpixel-operation down
docker-compose -p realpixel-operation up