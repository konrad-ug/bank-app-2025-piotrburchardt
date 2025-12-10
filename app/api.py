from flask import Flask, request, jsonify
from src.account import Account, BusinessAccount, AccountsRegistry

app = Flask(__name__)
registry = AccountsRegistry()


def _serialize_account(account):
    return {
        "type": "business" if isinstance(account, BusinessAccount) else "personal",
        "name": getattr(account, "first_name", getattr(account, "company_name", "")),
        "surname": getattr(account, "last_name", ""),
        "pesel": getattr(account, "pesel", None),
        "nip": getattr(account, "nip", None),
        "balance": account.balance,
    }


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json(force=True, silent=True) or {}
    account_type = data.get("type", "personal")

    if account_type == "business":
        if not data.get("company_name") or not data.get("nip"):
            return jsonify({"message": "company_name and nip are required"}), 400
        account = BusinessAccount(data["company_name"], data["nip"])
    else:
        if not data.get("name") or not data.get("surname") or not data.get("pesel"):
            return jsonify({"message": "name, surname and pesel are required"}), 400
        if registry.get_account_by_pesel(data["pesel"]):
            return jsonify({"message": "Account with this pesel already exists"}), 409
        account = Account(data["name"], data["surname"], data["pesel"], data.get("promo_code"))

    registry.add_account(account)
    return jsonify(_serialize_account(account)), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    return jsonify([_serialize_account(acc) for acc in accounts]), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    return jsonify({"count": registry.get_accounts_count()}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404
    return jsonify(_serialize_account(account)), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json(force=True, silent=True) or {}
    if isinstance(account, BusinessAccount):
        account.company_name = data.get("company_name", account.company_name)
    else:
        account.first_name = data.get("name", account.first_name)
        account.last_name = data.get("surname", account.last_name)

    return jsonify(_serialize_account(account)), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404

    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json(force=True, silent=True) or {}
    transfer_type = data.get("type")
    amount = data.get("amount")

    if transfer_type not in ("incoming", "outgoing", "express"):
        return jsonify({"message": "Invalid transfer type"}), 400

    if not isinstance(amount, (int, float)):
        return jsonify({"message": "amount is required"}), 400

    if transfer_type == "incoming":
        success = account.transfer_in(amount)
        if not success:
            return jsonify({"message": "Transfer failed"}), 400
    elif transfer_type == "outgoing":
        success = account.transfer_out(amount)
        if not success:
            return jsonify({"message": "Transfer failed"}), 422
    else:
        success = account.express_transfer_out(amount)
        if not success:
            return jsonify({"message": "Transfer failed"}), 422

    return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
