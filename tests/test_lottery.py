from brownie import accounts, config, lottery, network
from web3 import Web3


def test_lottery():
    account = accounts.add(config["wallets"]["from_key"])
    price = config["networks"][network.show_active()]["eth"]
    lottery_deploy = lottery.deploy(
        price,
        {"from": account},
    )

    assert lottery_deploy.getPrice() > Web3.toWei(0.01, "ether")
    assert lottery_deploy.getPrice() < Web3.toWei(0.02, "ether")
