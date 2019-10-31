#!/bin/bash

commoname=$(<server_id)
country=US
state=Illinois
locality=Chicago
organization="Last Stand Cloud"
organizationUnit="Last Stand User Server"
email=laststandcloud@protonmail.com

openssl req -new -key privkey.pem -out laststanduser.csr \
	-subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationUnit/CN=$commoname/emailAddress=$email"
 
exit 0