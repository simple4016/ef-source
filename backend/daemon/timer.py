import sys
sys.path.append('../common')  # noqa:E402
import threading
import argparse
import random
import const
from eth_api import eth_api
from handler import initial_token_address_table_usdc

from handler import calibrate_token_balance_usdc


from db_tables import db
from handler_wbtc import initial_token_address_table_wbtc
from handler_wbtc import calibrate_token_balance_wbtc
from handler_eth import  initial_token_address_table_eth
from handler_eth import calibrate_token_balance_eth
from db_tables import GasPrice




import handler
import handler_wbtc
import handler_eth


class repeat_timer(threading.Timer):
    def run(self):
        while True:
            self.function(*self.args, **self.kwargs)
            if not self.finished.wait(self.interval):
                continue


def run(ea,
        bid_filter_usdc, bid_filter_usdc_transfer,
        bid_filter_eth, bid_filter_eth_transfer,
        bid_filer_btc, bid_filter_btc_transfer):
    handler.handle_BidInfo(ea, bid_filter_usdc)
    handler.handle_BidInfo(ea, bid_filter_usdc_transfer)
    handler_eth.handle_BidInfo_eth(ea, bid_filter_eth)
    handler_eth.handle_BidInfo_eth(ea, bid_filter_eth_transfer)
    handler_wbtc.handle_BidInfo_wbtc(ea, bid_filer_btc)
    handler_wbtc.handle_BidInfo_wbtc(ea, bid_filter_btc_transfer)


    # handler.handle_Profit_info(ea)

    if random.random() > 1.0 * const.DAEMON_TIMER_IN_SECONDS / const.INFO_UPDATE_INTERVAL_IN_SECONDS:
        return
    handler.handle_Supply_info(ea)
    handler_eth.handle_Supply_info_eth(ea)
    handler_wbtc.handle_Supply_info_wbtc(ea)


def get_current_gas(ea):

    try:
        if ea :

            new_block_height, new_gas_price = ea.getGasPrice()

            newGas = GasPrice(id=1, block_height=new_block_height, gas_price=new_gas_price)

            db.session.merge(newGas)

            db.session.commit()

    except (TypeError, AttributeError):
        return






def timer(host, project_id):

    ea = eth_api(host, project_id)

    cff_contract_usdc = const.contract_CFVault_usdc[host]
    bid_filter_usdc = ea.create_filter('latest', 'latest', cff_contract_usdc, [
        [const.topic_CUserDeposit, const.topic_CUserWithdraw]])
    cff_contract_usdc_token = const.contract_CFToken_usdc[host]
    bid_filter_usdc_token = ea.create_filter('latest', 'latest', cff_contract_usdc_token, [
        [const.topic_CUserTransfer]])

    cff_contract_eth = const.contract_CFVault_eth[host]
    bid_filter_eth = ea.create_filter('latest', 'latest', cff_contract_eth, [
        [const.topic_CUserDeposit, const.topic_CUserWithdraw ]])
    cff_contract_eth_token = const.contract_CFToken_eth[host]
    bid_filter_eth_token = ea.create_filter('latest', 'latest', cff_contract_eth_token, [
        [const.topic_CUserTransfer]])

    cff_contract_wbtc = const.contract_CFVault_wbtc[host]
    bid_filter_wbtc = ea.create_filter('latest', 'latest', cff_contract_wbtc, [
        [const.topic_CUserDeposit, const.topic_CUserWithdraw ]])

    cff_contract_wbtc_token = const.contract_CFToken_wbtc[host]
    bid_filter_wbtc_token = ea.create_filter('latest', 'latest', cff_contract_wbtc_token, [
        [const.topic_CUserTransfer]])

    t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run, [ea, bid_filter_usdc,
                                                          bid_filter_usdc_token,
                                                          bid_filter_eth,
                                                          bid_filter_eth_token,
                                                          bid_filter_wbtc,
                                                          bid_filter_wbtc_token])
    t.start()

    t_gas = repeat_timer(const.DAEMON_TIMER_GAS_IN_SECONDS, get_current_gas,[ea])
    t_gas.start()


# def timer_earn(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract = const.contract_CFController_usdc[host]
#     bid_filter = ea.create_filter('latest', 'latest', cff_contract, [
#         [const.topic_earnCRV, const.topic_earnExtra]])
#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run_earn, [ea, bid_filter])
#     t.start()


# def timer_transfer(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract_usdc_token = const.contract_CFToken_usdc[host]
#     bid_filter_usdc_token = ea.create_filter('latest', 'latest', cff_contract_usdc_token, [
#         [const.topic_CUserTransfer]])
#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run, [ea, bid_filter])
#     t.start()

# def run_wbtc(ea, bid_filter):
#     handler_wbtc.handle_BidInfo_wbtc(ea, bid_filter)

#     # handler.handle_Profit_info(ea)

#     if random.random() > 1.0 * const.DAEMON_TIMER_IN_SECONDS / const.INFO_UPDATE_INTERVAL_IN_SECONDS:
#         return
#     handler_wbtc.handle_Supply_info_wbtc(ea)


# def timer_wbtc(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract = const.contract_CFVault_wbtc[host]
#     bid_filter = ea.create_filter('latest', 'latest', cff_contract, [
#         [const.topic_CUserDeposit, const.topic_CUserWithdraw, const.topic_CUserDepositFee ]])



#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run_wbtc, [ea, bid_filter])
#     t.start()


# def timer_transfer_wbtc(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract = const.contract_CFToken_wbtc[host]
#     bid_filter = ea.create_filter('latest', 'latest', cff_contract, [
#         [const.topic_CUserTransfer]])
#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run_wbtc, [ea, bid_filter])
#     t.start()




# def run_eth(ea, bid_filter):
#     handler_eth.handle_BidInfo_eth(ea, bid_filter)

#     # handler.handle_Profit_info(ea)

#     if random.random() > 1.0 * const.DAEMON_TIMER_IN_SECONDS / const.INFO_UPDATE_INTERVAL_IN_SECONDS:
#         return




# def timer_eth(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract = const.contract_CFVault_eth[host]
#     bid_filter = ea.create_filter('latest', 'latest', cff_contract, [
#         [const.topic_CUserDeposit, const.topic_CUserWithdraw, const.topic_CUserDepositFee ]])
#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run_eth, [ea, bid_filter])
#     t.start()


# def timer_transfer_eth(host, project_id):
#     ea = eth_api(host, project_id)
#     cff_contract = const.contract_CFToken_eth[host]
#     bid_filter = ea.create_filter('latest', 'latest', cff_contract, [
#         [const.topic_CUserTransfer]])
#     t = repeat_timer(const.DAEMON_TIMER_IN_SECONDS, run_eth, [ea, bid_filter])
#     t.start()


def main():
    parser = argparse.ArgumentParser(
        description='CFF', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--host', type=str, default='mainnet', help='network host connection')
    parser.add_argument('--project_id', type=str,
                        default='8dfb12dc6b8a4e6fa3e3480b7b646f12', help='infura project id')

    args = parser.parse_args()
    timer(args.host, args.project_id)

    # timer_transfer(args.host, '86b59cc988c54f8d9f0f72f7562ea628')
    # timer_wbtc(args.host, 'e592214f63ee46c7acdd532f0270dd72')
    # timer_transfer_wbtc(args.host, '0ade24290ecf4d7b9eb6c682d32c3f5e')

    # timer_eth(args.host, 'aea3344a746341df94fed88f47e620e0')
    # timer_transfer_eth(args.host, '86b59cc988c54f8d9f0f72f7562ea628')


    # initial_token_address_table_usdc()
    # initial_token_address_table_wbtc()

    # ea = eth_api('ropsten', '9543b9089f07402fb367f5b9c37d28a2')
    # calibrate_token_balance_usdc(ea)
    # calibrate_token_balance_wbtc(ea)


if __name__ == '__main__':
    main()
