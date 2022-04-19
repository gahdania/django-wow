export UIID=5000
export GID=5000
export HOST_NAME=mail.gahd.io
export DOMAIN_NAME=gahd.io
export NETWORK=192.168.99.0/24
export COUNTRY=US
export PROVIDENCE_STATE=Virginia
export LOCALITY=Springifeld
export ORGANIZATION=GAHD.IO
export SUBJECT="/C=${COUNTRY}/ST=${PROVIDENCE_STATE}/L=${LOCALITY}/O=${ORGANIZATION}/CN=${HOST_NAME}"
export MAIL_DB_HOST=192.168.99.2
export MAIL_DB_USER=postfix
export MAIL_DB_PASS=testpass
export MAIL_DB_NAME=postfix

sed -ri -e "s/<MAIL_DB_USER>/$MAIL_DB_USER/g" -e "s/<MAIL_DB_PASS>/$MAIL_DB_PASS/g" \
    -e "s/<MAIL_DB_NAME>/$MAIL_DB_NAME/g" -e "s/<MAIL_DB_HOST>/$MAIL_DB_HOST/g" *.cf

sed -ri -e "s/<UID>/$UIID/g" -e "s/<GID>/$GID/g" -e "s/<HOST_NAME>/$HOST_NAME/g" \
        -e "s/<DOMAIN_NAME>/$DOMAIN_NAME/g" -e "s/<NETWORK>/$NETWORK/g" main.txt

