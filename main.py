# Author: luedi

import json
from fastapi import FastAPI
from pydantic import BaseModel
from requests  import get,put
from requests.exceptions import RequestException
app = FastAPI()


print("RDDNS Version: V0.2.7")

class aItem(BaseModel):
    ip: str
    token: str

def getCFDnsDetails(domain:str,zone_id:str,email:str,api_key:str):
    try:
        with get("https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records",
                                  headers={
                                      "X-Auth-Email":email,
                                      "X-Auth-Key":api_key,
                                  }) as result:
            records = [i for i in result.json()["result"] if i["name"]==domain]
            if not records:
                print(f"[WARN] DNS record not found for domain: {domain}")
                return None

            return records[0]
    except RequestException as e:
        print(e)
        return None
def changeIP(zone_id:str,record_id:str,email:str,api_key:str,bodyjson:dict):
    try:
        with put("https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records/"+record_id,
                 headers={
                     "X-Auth-Email":email,
                     "X-Auth-Key":api_key,
                 },json=bodyjson) as result:
            return result.json()["result"]
    except RequestException as e:
        print(e)
        return False


@app.post("/ipnew")
async def ipnew(item: aItem):
    with open('production.json') as f:
        Config = json.load(f)
        print("UpdateConfig:", Config)
    if item.token != Config["token"]:
        return {"code": 2}
    print("New IP Request:",item.ip)
    for i in Config["domains"]:
        resp=getCFDnsDetails(i["domain"],Config["zone_id"],Config["email"],Config["api_key"])
        if resp["content"] == item.ip:
            print("IP not change:",i["domain"])
            continue
        res=changeIP(Config["zone_id"],resp['id'],Config["email"],Config["api_key"],{
            "type": resp["type"],
            "name": resp["name"],
            "ttl": resp["ttl"],
            "content": item.ip,
            "proxied": resp["proxied"]
        })
        print("Detail:",resp)
        print("Result:", res)

        if (not res or not resp):
            return {"code": 0}


    return {"code": 1}
