import json
import time
import requests

import jtool.dbc as dbc

BASE_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,el;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

PARAMS = {
    "format": "geojson",
    "addressdetails": 0,
    "polygon": 0,
    "limit": 1
}

SESS = requests.Session()
SESS.headers = HEADERS
SESS.params = PARAMS


def get_geojson(addr, sleep=1) -> dict:
    global SESS
    SESS.params['q'] = addr
    resp = SESS.get(BASE_URL)
    if sleep:
        time.sleep(sleep)
    resp.raise_for_status()
    return resp.json()


def gen_rows():
    sql = """
    select node_id, json_value(properties, '$.address') from node
    where json_path_exists(properties, '$.address')=1;
    """
    with dbc.get_cur() as cur:
        cur.execute(sql)
        return cur.fetchall()


def write_json(fn, obj):
    with open(fn, 'w') as fh:
        json.dump(obj, fh)
    print('write to', fn, 'done')


if __name__ == '__main__':
    skip_me = "Portcullis TrustNet Chambers P.O. Box 3444 Road Town, Tortola BRITISH VIRGIN ISLANDS"
    print('starting nominatim requests...')
    seen_addrs = set()
    for nid, addr in gen_rows():
        if not addr:
            continue
        if addr in seen_addrs:
            continue
        if skip_me in addr:
            continue
        seen_addrs.add(addr)
        fn = f'nom_out/{nid}.json'
        try:
            j_resp = get_geojson(addr)
            feats = j_resp.get('features', [])
            if len(feats) > 0:
                write_json(fn, j_resp)
        except Exception as e:
            print('ERROR', e)
            write_json(f'nom_out/ERROR_{nid}.json', {'error': str(e)})

    print('finished nominatim')
    print()
