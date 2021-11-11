from brownie import accounts, network, config


FORKED_LOCAL_BLOCKCHAINS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAINS_ENVIRONMENT = ["development", "ganache-local"]


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAINS_ENVIRONMENT
        or network.show_active() in FORKED_LOCAL_BLOCKCHAINS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}


def get_contract(contract_name):
    """This function will garab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of the contract, and
    return that mock contract.

        Args:
            contract_name(string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
            MockV3Aggregator[-1]
    """
