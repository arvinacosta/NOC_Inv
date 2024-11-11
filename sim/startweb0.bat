cls

echo     App Running @ Port 8872

uvicorn main2:app --host 0.0.0.0 --port 8872 --reload --ssl-keyfile=certs/server_unencrypted.key --ssl-certfile=certs/server.crt
