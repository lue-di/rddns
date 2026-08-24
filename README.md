# Redirect DDNS
This project depends on RouterOS or other Systems because this project needs to be called by other systems.
So your RouterOS has to call this project's api when ip changes.

# Usage
Configure your routeros's scheduler according to example.rsc .

Put only service settings and DNS domains in `production.json`; credentials must be supplied with environment variables:

```bash
export TOKEN="your-ddns-token"
export EMAIL="your-cloudflare-email"
export API_KEY="your-cloudflare-api-key"
```

Then deploy this project to your server. For Docker, mount `production.json` and pass the same values with `-e TOKEN=... -e EMAIL=... -e API_KEY=...`:

```bash
docker run -d --name rddns -p 8181:8181 \
  -v "$(pwd)/production.json:/rddns/production.json:ro" \
  -e TOKEN="your-ddns-token" \
  -e EMAIL="your-cloudflare-email" \
  -e API_KEY="your-cloudflare-api-key" \
  1uedi/rddns
```

You can use [docker](https://hub.docker.com/r/1uedi/rddns) to deploy this project.

# issue
The project is for my personal use.
So it may not be stable.
If you have any problem, please open an issue.
Or if you have any suggestion, please open a pull request or open an issue.
