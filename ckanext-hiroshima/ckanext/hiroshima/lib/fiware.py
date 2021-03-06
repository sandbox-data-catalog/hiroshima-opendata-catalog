# -*- coding: utf-8 -*-
import requests
import ckan.lib.base as base
from ckan.common import config
import datetime

def getdata(type, id, attrName):
    
    fiwareFqdn = config.get('fiware.comet.fqdn')
    fiwareService = config.get('fiware.service')
    fiwarePath = config.get('fiware.path')

    datato = datetime.datetime.now()
    # 実証実験のサンプルデータが揃うまで、2020年8月30日固定にする。
    # 正式なデータが返ってくるようになったときに削除
    datato = datato.replace(year=2020, month=8, day=30)

    # 16時間くらいがグラフ上のプロットの数がちょうど良いとのこと
    #datafrom = datato + datetime.timedelta(days=-1)
    datafrom = datato + datetime.timedelta(hours=-16)

 
    headers = {'Fiware-Service': fiwareService, 'Fiware-Servicepath': fiwarePath}
    url = fiwareFqdn + '/STH/v1/contextEntities/type/' + type + '/id/' + id + '/attributes/' + attrName + '?lastN=100&dateFrom=' + datafrom.strftime("%Y-%m-%dT%H:%M:%SZ") + '&dateTo=' + datato.strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        r = requests.get(url, headers=headers)

        if r.status_code in (400, 403, 405):
            r.raise_for_status()

    except requests.exceptions.HTTPError as error:
        details = 'Could not proxy resource. Server responded with %s %s' % (
            error.response.status_code, error.response.reason)
        base.abort(409, detail=details)
    except requests.exceptions.ConnectionError as error:
        details = '''Could not proxy resource because a
                            connection error occurred. %s''' % error
        base.abort(502, detail=details)
    except requests.exceptions.Timeout as error:
        details = 'Could not proxy resource because the connection timed out.'
        base.abort(504, detail=details)

    return r
