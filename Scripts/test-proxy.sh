#!/bin/bash

#
#  test-proxy.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

# GET /watch/ticker
curl --location 'http://10.0.0.7:80/watch/MSFT'
# GET /watch/ticker?avg=<num>
curl --location 'http://10.0.0.7:80/watch/MSFT?avg=3'
# PUT /user/email
# -- ticker
curl --location --request PUT 'http://10.0.0.7:80/users/alessio198@gmail.com' \
--header 'Content-Type: text/plain' \
--data 'MSFT'
# DELETE /user/email
curl --location --request DELETE 'http://10.0.0.7:80/users/alessio198@gmail.com'