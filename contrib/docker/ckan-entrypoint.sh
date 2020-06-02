#!/bin/sh

ckan-paster --plugin=ckan db init -c "${CKAN_CONFIG}/ckan.ini"
exec "$@"
