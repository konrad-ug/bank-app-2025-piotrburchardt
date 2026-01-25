from src.account import Account
from src.accounts_repository import MongoAccountsRepository


def test_save_all_clears_and_upserts(mocker, personal_account):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository(collection=mock_collection)
    personal_account.history = [100.0, -50.0]
    personal_account.balance = 50.0

    repo.save_all([personal_account])

    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.update_one.assert_called_once()
    filter_arg, update_arg = mock_collection.update_one.call_args[0]
    assert filter_arg == {"pesel": personal_account.pesel}
    assert update_arg["$set"]["balance"] == 50.0
    assert update_arg["$set"]["history"] == [100.0, -50.0]


def test_load_all_returns_accounts_with_data(mocker):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = [
        {
            "first_name": "A",
            "last_name": "B",
            "pesel": "12345678901",
            "balance": 75.0,
            "history": [75.0],
        }
    ]
    repo = MongoAccountsRepository(collection=mock_collection)

    accounts = repo.load_all()

    assert len(accounts) == 1
    account = accounts[0]
    assert account.first_name == "A"
    assert account.last_name == "B"
    assert account.pesel == "12345678901"
    assert account.balance == 75.0
    assert account.history == [75.0]


def test_constructor_creates_collection_when_none(mocker):
    mock_client = mocker.MagicMock()
    mock_db = mocker.MagicMock()
    mock_collection = mocker.Mock()
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    mocker.patch("src.accounts_repository.MongoClient", return_value=mock_client)

    repo = MongoAccountsRepository()

    assert repo._collection is mock_collection
    mock_client.__getitem__.assert_called_once_with("bank_app")
    mock_db.__getitem__.assert_called_once_with("accounts")
