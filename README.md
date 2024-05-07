# HookBridge
A configurable webhook bridge. Routes HTTP webhooks from any source, to any HTTP REST/JSON destination !

## Usage
1. Define your routes in a `routes.json` file (see **Configuration**)
2. Start the bridge using Docker :

```shell
docker run -itd -p 8080:80 -v $(pwd)/routes.json:/app/routes.json:ro ghcr.io/lgatellier/hookbridge
```
3. Configure your source webhooks to hit http://hostname:8080/route/route_name
4. Enjoy !

### Supported tags
Currently supported tags :
- `v0.2.0`

**DISCLAIMER :** This project has not been released in a stable version yet. Breaking changes can still occur until version `1.0.0` is released.

## Configuration
You can configure the bridge using a single JSON file (usually named `routes.json`). Here is an example file :
```json
{
    "example_route": {
        "auth_headers": {
            "X-Api-Token": "#env[EXAMPLE_ROUTE_TOKEN]"
        },
        "input": {
            "body": {
                "$.source_name": {
                    "type": "equalsTo",
                    "equalsTo": "mysource",
                    "context_variable": "SOURCE_NAME"
                }
            }
        },
        "output": {
            "gitlab": {
                "url": "https://gitlab.com/api/v4/projects/my%2Fproject%2Fid/issues",
                "headers": {
                    "Private-Token": "#env[GITLAB_API_TOKEN]"
                },
                "body": {
                    "title": "Hook received from #context[SOURCE_NAME]"
                }
            }
        }
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

### Routes
The routes.json file describes all the available routes in your bridge. Each route has a name, and some input and output configuration parameters :
- `auth_headers` : the HTTP headers used for clients authentication. You can define here, for example, an API token (often sent by the webhook emitters)
- `input` : some rules and conditions to apply to all received requests. See **inputs**.
- `output` : a list of webhooks to trigger when a valid (see **inputs**) request is received. See **outputs**.

### Inputs
The input rules describe :
- The checks to apply to each received request. The checks results can lead to request rejection with `HTTP 400` error
- The JSON fields to capture, to be set later in the outputs. See **Variables injection**

The `input` configuration can only handle a `body` field. Applying checks or captures on HTTP headers is not possible at the moment.

Each key/value pair under the `input[body]` object is made of :
- A JSONPath-string key, which describes the JSON field on which the input rule will be applied
- A JSON value object, which describes the check and variable definition which will be applied to the selected value
-
```json
{
    "input": {
        "body": {
            "$.source_name": {
                "type": "equalsTo",
                "equalsTo": "mysource",
                "context_variable": "SOURCE_NAME"
            },
            "id": "present"
        }
    }
}
```

#### Rule type
The minimum description for a rule is its type. The bridge handles only 2 types at the moment :
- `present` : The field designated by the JSONPath must exist in all received requests
- `equalsTo` :  The field designated by the JSONPath must be equal to the associated `equalsTo` JSON property

The type can be specified by the `type` property. The `type` property can be omitted if :
- The rule type takes no parameter (ex: the `present` rule type). In this case, the rule type can be specified directly as rule configuration object. Ex :
```json
{
    "$.source_name": "present"
}
```
- The first JSON property of the rule is the type name. Ex :
```json
{
    "$.source_name": {
        "equalsTo": "mysource",
        "context_variable": "SOURCE_NAME"
    }
}
```

#### Context variable
The `context_variable` field defines the name of the context variable where the request field value will be stored. This variable definition allows you to inject this value in the outputs using **Variables injection**

### Outputs
The output rules describes which HTTP endpoints must be called when a request is received on the route endpoint.

The `output` property is a JSON object. Each property of this object describes an endpoint to call. The property key is the output rule name (for logging/error handling), while the property value is a JSON object whose properties are :
- `url` : webhook destination endpoint
- `headers` (optional): the HTTP headers to set when sending a request to this endpoint. This property is a JSON object, with a key/value pair for each request header definition
- `body`: the JSON body to be sent to this endpoint
- `context_variables` (optional): The response fields to store into some context variables. This property is a JSON object defining, for each key/value pair :
  - Key : A JSONPath, describing the field to store
  - Value : The name of the variable where to store the selected field value

You can use **Variables injection** in `headers` and `body` properties.

### Variables injection
You can inject 2 types of variables in output bodies and headers :
- Environment variables : use `#env[VARIABLE_NAME]` syntax in your configuration
- Context variables, when defined in `input` rules : use `#context[VARIABLE_NAME]` syntax in your configuration

#### Output rules ordering
The JSON file is loaded into a Python [`OrderedDict`][1], thus the output endpoints are called in the order they are declared in the `routes.json` file.

[1]: https://docs.python.org/3/library/collections.html#collections.OrderedDict
