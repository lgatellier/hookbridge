# Webhook Gateway
A configurable webhook gateway. Routes HTTP webhooks from any source, to any HTTP REST/JSON destination !

## Usage
1. Define your routes in a `routes.json` file (see **Configuration**)
1. Start the gateway using Docker :

```shell
docker run -itd -p 8080:80 -v $(pwd)/routes.json:/app/routes.json:ro lgatellier/webhook-gateway
```
1. Configure your source webhooks to hit http://hostname:8080/route/route_name
1. Enjoy !

## Configuration
You can configure the gateway using a single JSON file (usually named `routes.json`). Here is an example file :
```json
{
    "example_route": {
        "auth_headers": {
            "X-Api-Token": "#env[EXAMPLE_ROUTE_TOKEN]"
        },
        "input": {
            "body": {
                "$.source_name": {
                    "equalsTo": "mysource",
                    "context_variable": "SOURCE_NAME"
                }
            }
        },
        "output": [{
            "name": "gitlab",
            "url": "https://gitlab.com/api/v4/projects/my%2Fproject%2Fid/issues",
            "headers": {
                "Private-Token": "#env[GITLAB_API_TOKEN]"
            },
            "body": {
                "title": "Hook received from #context[SOURCE_NAME]"
            }
        }]
    }
}
```

This example configuration defines a webhook endpoint with the following behavior/characteristics :
- The endpoint URL will be http://hostname:port/route/example_route
- All webhooks sent to this endpoint must have :
  - A `X-Api-Token` HTTP header which value is stored in the `EXAMPLE_ROUTE_TOKEN` environment variable
  - A `source_name` field at the top level of the JSON body, which value must be `mysource`
- For each received HTTP request, an HTTP call will be sent to gitlab.com API, to create an issue :
  - On `my/project/id` project
  - With a Private Access Token which value is stored in the GITLAB_API_TOKEN environment variable
  - The sent JSON body will contain a unique field `title`, containing the `source_name` field received in initial request
