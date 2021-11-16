from brownie import accounts, network, config, Lottery
import time
from brownie.network.main import show_active
from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.start({"from": account})
    tx.wait(1)
    print("Lottery has started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.minimumValue() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You have entered the lottery!")


def end_lotery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_lottery = lottery.end({"from": account})
    ending_lottery.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lotery()
