import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.simple_counter.client import (
        SimpleCounterClient,
    )

    app_client = SimpleCounterClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )
    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    # Lets call the increment function
    response = app_client.increment_global()
    logger.info(
        f"Called increment function on {app_spec.contract.name} ({app_client.app_id}) "
        f"received: {response.return_value}"
    )
    
    # Let's call it again
    response = app_client.increment_global()
    logger.info(
        f"Called increment function on {app_spec.contract.name} ({app_client.app_id}) "
        f"received: {response.return_value}"
    )

    # now we'll call decrement function
    response = app_client.decrement_global()
    logger.info(
        f"Called decrement function on {app_spec.contract.name} ({app_client.app_id}) "
        f"received: {response.return_value}"
    )

