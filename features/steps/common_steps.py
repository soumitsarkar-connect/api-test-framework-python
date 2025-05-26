import os
from behave import given, when, then
import configparser
import json
from jsonschema import validate, ValidationError
from helpers.api_helper import APIClient
from helpers.log_helper import Logger

logger = Logger("step-defs").get_logger()

# Store dynamic variables
stored_values = {}

config = configparser.ConfigParser()
config.read("configs/config.ini")
base_url = config["default"]["base_url"]
api_client = APIClient(base_url)

@given('I set request headers to')
def step_set_headers(context):
    headers = json.loads(context.text)
    api_client.set_headers(headers)

@when('I send a {method} request to "{endpoint}"')
def step_send_request(context, method, endpoint):
    endpoint = endpoint.format(**stored_values)
    context.response = api_client.request(method, endpoint)

@when('I send a {method} request to "{endpoint}" with payload')
def step_send_request_with_payload(context, method, endpoint):
    endpoint = endpoint.format(**stored_values)
    payload = json.loads(context.text)
    context.response = api_client.request(method, endpoint, data=payload)

@then('the response status code should be {status_code}')
def step_check_status_code(context, status_code):
    actual = context.response.status_code
    logger.info(f"Asserting status code: expected {status_code}, got {actual}")
    assert actual == int(status_code), f"Expected {status_code}, got {actual}"
    
@then('I store the value of "{response_key}" as "{alias}"')
def step_store_value(context, response_key, alias):
    value = context.response.json().get(response_key)
    logger.info(f"Storing response value: {response_key} = {value} as {alias}")
    assert value is not None, f"Response does not contain key '{response_key}'"
    stored_values[alias] = value

@then('the response should contain "{field}" with value "{expected_value}"')
def step_check_response_field(context, field, expected_value):
    expected_value = expected_value.format(**stored_values)
    json_body = context.response.json()
    actual_value = str(json_body.get(field, ''))
    logger.info(f"Asserting field '{field}': expected '{expected_value}', got '{actual_value}'")
    assert actual_value == expected_value, \
        f"Expected {field} to be {expected_value}, got {actual_value}"
    
@then('the response should match JSON schema "{schema_file}"')
def step_validate_schema(context, schema_file):
    schema_path = os.path.join("data", "json-schemas", schema_file)
    with open(schema_path) as f:
        schema = json.load(f)

    response_json = context.response.json()

    try:
        validate(instance=response_json, schema=schema)
        logger.info(f"Schema validation passed for: {schema_file}")
    except ValidationError as e:
        logger.error(f"Schema validation failed: {e.message}")
        raise AssertionError(f"JSON schema validation error: {e.message}")
