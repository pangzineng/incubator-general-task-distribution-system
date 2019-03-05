docker ps -a -q | % { docker rm $_ }
docker images | ConvertFrom-String | where {$_.P2 -eq "<none>"} | % { docker rmi $_.P3 }

$GTDS_DEFINITIONS = [IO.File]::ReadAllText("example/adboard-marketplace/definitions.yaml")

## build 
docker build --build-arg DEFINITIONS="$GTDS_DEFINITIONS" --build-arg VERSION=0.1.0 --build-arg SERVER_HOST=localhost --build-arg SERVER_PORT=8888 --build-arg SERVRE_BASE_PATH=v1 --build-arg CUSTOM_KEY=adslot:_adboard -t gtds-adboard-marketplace:0.1.0 ../../
 
## run locally
docker-compose -p gtds-adboard-marketplace down
docker-compose -p gtds-adboard-marketplace up