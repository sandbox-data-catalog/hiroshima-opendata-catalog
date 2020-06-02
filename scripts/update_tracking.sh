#!/bin/bash

. /usr/lib/ckan/default/bin/activate

cd /usr/lib/ckan/default/src/

paster --plugin=ckan tracking update -c /usr/lib/ckan/default/src/ckan/config/development.ini
paster --plugin=ckan search-index rebuild -r -c /usr/lib/ckan/default/src/ckan/config/development.ini

deactivate
