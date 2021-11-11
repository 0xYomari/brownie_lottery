from brownie import accounts, network, config, lottery
from scripts.helpful_scripts import get_account


def lottery():
    account = get_account()
    lottery_deploy = lottery.deploy(get_contract())


def main():
    lottery()
