# aiohttpapi

PG_DSN - enter your postgres in docker ip

run app
```
curl --location --request POST 'http://0.0.0.0:8080/post' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "title": "title",
    "id": "11",
    "author": "author"
}'
```
