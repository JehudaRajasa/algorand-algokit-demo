import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts.simple_counter import contract as simple_counter_contract


@pytest.fixture(scope="session")
def simple_counter_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return simple_counter_contract.app.build(algod_client)


@pytest.fixture(scope="session")
def simple_counter_client(
    algod_client: AlgodClient, simple_counter_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=simple_counter_app_spec,
        signer=get_localnet_default_account(algod_client),
    )
    client.create()
    return client


def test_says_hello(simple_counter_client: ApplicationClient) -> None:
    result = simple_counter_client.call(simple_counter_contract.hello, name="World")

    assert result.return_value == "Hello, World"
