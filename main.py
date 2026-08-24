# Author: luedi

import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests import get, put
from requests.exceptions import RequestException

from logger import setup_logging, get_logger

logger = setup_logging()

app = FastAPI()

# ── Read version from VERSION file ─────────────────────────────
__version__ = "unknown"
_version_path = Path(__file__).resolve().parent / "VERSION"
if _version_path.exists():
    __version__ = _version_path.read_text().strip()
else:
    # Fallback: get version from git tags (local development)
    try:
        import subprocess
        _tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, check=True,
            cwd=Path(__file__).parent
        ).stdout.strip().lstrip("v")
        if _tag:
            __version__ = _tag
    except Exception:
        pass
logger.info("RDDNS Version: V%s", __version__)

class aItem(BaseModel):
    ip: str
    token: str

def getCFDnsDetails(domain: str, zone_id: str, email: str, api_key: str):
    try:
        with get(
            "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records",
            headers={
                "X-Auth-Email": email,
                "X-Auth-Key": api_key,
            },
        ) as result:
            data = result.json()
            if not data.get("success") or data.get("result") is None:
                logger.error(
                    "Cloudflare API request failed (HTTP %s): %s",
                    result.status_code,
                    data.get("errors"),
                )
                return None
            records = [i for i in data["result"] if i["name"] == domain]
            if not records:
                logger.warning("DNS record not found for domain: %s", domain)
                return None

            return records[0]
    except RequestException as e:
        logger.error("Failed to query Cloudflare DNS for %s: %s", domain, e)
        return None


def changeIP(zone_id: str, record_id: str, email: str, api_key: str, bodyjson: dict):
    try:
        with put(
            "https://api.cloudflare.com/client/v4/zones/"
            + zone_id
            + "/dns_records/"
            + record_id,
            headers={
                "X-Auth-Email": email,
                "X-Auth-Key": api_key,
            },
            json=bodyjson,
        ) as result:
            data = result.json()
            if not data.get("success"):
                logger.error(
                    "Cloudflare API update failed (HTTP %s): %s",
                    result.status_code,
                    data.get("errors"),
                )
                return False
            return data["result"]
    except RequestException as e:
        logger.error("Failed to update Cloudflare DNS record %s: %s", record_id, e)
        return False


@app.post("/ipnew")
async def ipnew(item: aItem):
    token = os.getenv("TOKEN")
    email = os.getenv("EMAIL")
    api_key = os.getenv("API_KEY")
    missing_variables = [
        name
        for name, value in (("TOKEN", token), ("EMAIL", email), ("API_KEY", api_key))
        if not value
    ]
    if missing_variables:
        logger.error("Missing required environment variables: %s", ", ".join(missing_variables))
        raise HTTPException(
            status_code=500,
            detail=f"Missing required environment variables: {', '.join(missing_variables)}",
        )

    with open("production.json") as f:
        config = json.load(f)
        logger.debug("UpdateConfig loaded with %d domain(s)", len(config.get("domains", [])))
    if item.token != token:
        logger.warning("Token mismatch for IP request from %s", item.ip)
        return {"code": 2}
    logger.info("New IP request: %s", item.ip)
    for i in config["domains"]:
        resp = getCFDnsDetails(i["domain"], i["zone_id"], email, api_key)
        if not resp:
            logger.warning("DNS record not found, skip: %s", i["domain"])
            continue
        if resp["content"] == item.ip:
            logger.info("IP unchanged for %s (%s)", i["domain"], item.ip)
            continue
        res = changeIP(
            i["zone_id"],
            resp["id"],
            email,
            api_key,
            {
                "type": resp["type"],
                "name": resp["name"],
                "ttl": resp["ttl"],
                "content": item.ip,
                "proxied": resp["proxied"],
            },
        )
        logger.debug("Record detail for %s: %s", i["domain"], resp)
        logger.debug("Update result for %s: %s", i["domain"], res)
        logger.info("IP changed for %s", i["domain"])
        if not res or not resp:
            return {"code": 0}

    return {"code": 1}
