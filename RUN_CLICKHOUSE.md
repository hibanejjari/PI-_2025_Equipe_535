```shell
docker run -d `
  --name clickhouse-server `
  -p 8123:8123 `
  -p 9000:9000 `
  -e CLICKHOUSE_PASSWORD="1234" `
  --ulimit nofile=262144:262144 `
  clickhouse/clickhouse-server:latest
```