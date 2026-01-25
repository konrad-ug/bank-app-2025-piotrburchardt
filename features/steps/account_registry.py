from behave import given, when, then, step
import requests

URL = "http://127.0.0.1:5000"


def _get_account(pesel):
    return requests.get(f"{URL}/api/accounts/{pesel}")


@when('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
@given('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {"name": name, "surname": last_name, "pesel": pesel}
    create_resp = requests.post(f"{URL}/api/accounts", json=json_body)
    assert create_resp.status_code == 201
    context.last_response = create_resp


@given("Account registry is empty")
@step("Account registry is empty")
@step("Accoount registry is empty")
@step("Acoount registry is empty")
def clear_account_registry(context):
    response = requests.get(f"{URL}/api/accounts")
    assert response.status_code == 200

    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(f"{URL}/api/accounts/{pesel}")


@then('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(f"{URL}/api/accounts/count")
    assert response.status_code == 200
    data = response.json()
    assert str(data.get("count")) == count


@then('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = _get_account(pesel)
    assert response.status_code == 200


@then('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = _get_account(pesel)
    assert response.status_code == 404


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(f"{URL}/api/accounts/{pesel}")
    assert response.status_code == 200
    context.last_response = response


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = {field: value}
    response = requests.patch(f"{URL}/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200
    context.last_response = response


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = _get_account(pesel)
    assert response.status_code == 200
    data = response.json()

    if field not in data:
        raise AssertionError(f"Field '{field}' not found in account data")

    expected_value = float(value) if field == "balance" else value
    assert data[field] == expected_value


@when('I make "{transfer_type}" transfer of "{amount}" for account with pesel: "{pesel}"')
@given('I make "{transfer_type}" transfer of "{amount}" for account with pesel: "{pesel}"')
@step('I make "{transfer_type}" transfer of "{amount}" for account with pesel: "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    payload = {"type": transfer_type, "amount": float(amount)}
    response = requests.post(f"{URL}/api/accounts/{pesel}/transfer", json=payload)
    context.last_response = response


@then('Transfer response code equals: "{status_code}"')
def transfer_response_code(context, status_code):
    assert hasattr(context, "last_response"), "No response recorded on context"
    assert context.last_response.status_code == int(status_code)


@then('Transfer response message equals: "{message}"')
def transfer_response_message(context, message):
    assert hasattr(context, "last_response"), "No response recorded on context"
    data = context.last_response.json()
    assert data.get("message") == message
