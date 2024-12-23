#!/bin/bash

#
#  test-proxy.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

# GET /stocks/ticker
curl --location 'http://10.0.0.7:80/watch/MSFT'
# GET /stocks/ticker?avg=<num>
curl --location 'http://10.0.0.7:80/watch/MSFT?avg=3'
# PUT /users/device_id
# -- ticker
curl --location --request PUT 'http://10.0.0.7:80/users/alessio198@gmail.com' \
--header 'Content-Type: text/plain' \
--data 'MSFT'
# PUT /users/device_id
# -- { "ticker": _, "device_token": _, "low_value": _, "high_value": _ }
curl --location --request PUT 'http://10.0.0.17:80/users/alessio198@gmail.com' \
--header 'Content-Type: application/json' \
--data '{
    "ticker": "MSFT",
    "device_token": "e5b4c3a2d9f8172e9fcb30855f3e5b4c3a2d9f8172e9fcb30855f3e5b4c3a2d9",
    "high_value": 400.5,
    "low_value": 110.1
}'
# DELETE /users/device_id
curl --location --request DELETE 'http://10.0.0.7:80/users/alessio198@gmail.com'