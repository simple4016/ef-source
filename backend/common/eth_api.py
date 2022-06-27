from web3 import Web3
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes
import const
from datetime import datetime
from dateutil import tz
import pytz
import requests
import json


class eth_api:

    def __init__(self, host, project_id):
        assert isinstance(host, str)
        assert isinstance(project_id, str)
        self.host = host
        self.wss = self.__websocket_provider(host, project_id)
        self.w3 = self.wss
        #self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def __websocket_provider(self, host, project_id):
        url = 'wss://%s.infura.io/ws/v3/%s' % (host, project_id)
        return Web3(Web3.WebsocketProvider(url))

    def get_block(self, symbol):
        return self.w3.eth.getBlock(symbol)

    def get_deposit_to(self, txh):
        logs = self.w3.eth.getTransactionReceipt(txh)['logs']
        for log in reversed(logs):
            if log['topics'][0].hex() == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
                return log['topics'][2].hex()[-40:]


    def get_block_height(self):
        block = self.get_block('latest')
        assert 'number' in block
        return block['number']

    def get_block_time(self):
        block = self.get_block('latest')
        assert 'timestamp' in block
        return block['timestamp']

    def readonly_contract(self, contract_addr, data):
        return self.eth_call({'to': contract_addr, 'data': data})

    def eth_call(self, transaction):
        return self.w3.eth.call(transaction)

    def __check_filter_params(self, key, val, d):
        if val:
            d.update({key: val})
        return d

    def create_filter(self, block_s, block_e, address, topics):
        d = self.__check_filter_params('fromBlock', block_s, dict())
        d = self.__check_filter_params('toBlock', block_e, d)
        d = self.__check_filter_params('address', address, d)
        d = self.__check_filter_params('topics', topics, d)
        return self.wss.eth.filter(d)

    def get_filter_changes(self, filter_id):
        return self.wss.eth.getFilterChanges(filter_id)

    def getGasPrice(self):

        url = 'https://api.etherscan.io/api'

        data = {'module':'gastracker',
            'action':'gasoracle',
            'apikey':'R7597ZRXX8FMPYV7UCKY7T8RHSZ7UC92MW'}

        response = requests.post(url, data=data)

        if (response.status_code != 204 and response.headers["content-type"].strip().startswith("application/json")):

            try:

                results_json = json.loads(response.text)
                return  results_json['result']['LastBlock'], results_json['result']['ProposeGasPrice']
            except ValueError:
        # decide how to handle a server that's misbehaving to this extent
                return 100,100




def split_by_32bytes(data):
    step = const.PARAMS_BYTES_IN_HEX_LENGTH
    return [data[i:i+step] for i in range(0, len(data), step)]


def balanceOf(ea, contract_addr, address):
    method_id = '0x%s' % const.hash_balanceOf[:8]
    data = str(address[2:]).zfill(const.PARAMS_BYTES_IN_HEX_LENGTH)
    data = method_id + data
    balance_byte = ea.readonly_contract(contract_addr, data)
    return int(balance_byte.hex(), 16)


def totalSupply(ea, contract_addr):
    supply_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_totalSupply[:8])
    return int(supply_byte.hex(), 16)


def decimals(ea, contract_addr):
    decimals_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_decimals[:8])
    return int(decimals_byte.hex(), 16)


def getPricePerFullShare(ea, contract_addr):
    per_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_getPricePerFullShare[:8])
    return int(per_byte.hex(), 16)


def underlying_balance(ea, contract_addr):
    balance_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_underlying_balance[:8])
    return int(balance_byte.hex(), 16)


def getVirtualPrice(ea, contract_addr):
    price_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_get_virtual_price[:8])
    return int(price_byte.hex(), 16)


def getWithdraweeRatio(ea, contract_addr):
    price_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_get_withdraw_fee_ratio[:8])
    return int(price_byte.hex(), 16)


def getDecimal(ea, contract_addr):
    decimal_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_getDecimal[:8])
    return int(decimal_byte.hex(), 16)


def getCurrentPeriod(ea, contract_addr):
    period_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_getCurrentPeriod[:8])
    return int(period_byte.hex(), 16)


def getCurrentPeriodStartBlock(ea, contract_addr):
    period_byte = ea.readonly_contract(contract_addr, '0x%s' %
                                       const.hash_getCurrentPeriodStartBlock[:8])
    return int(period_byte.hex(), 16)


def balance(ea, contract_addr):
    balance_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_balance[:8])
    return int(balance_byte.hex(), 16)


def getParamPeriodBlockNum(ea, contract_addr):
    num_byte = ea.readonly_contract(contract_addr, '0x%s' % const.hash_getParamPeriodBlockNum[:8])
    return int(num_byte.hex(), 16)


def sratios(ea, contract_addr, index):
    method_id = '0x%s' % const.hash_sratios[:8]
    data = hex(index)[2:].zfill(const.PARAMS_BYTES_IN_HEX_LENGTH)
    data = method_id + data
    sratios_byte = ea.readonly_contract(contract_addr, data)
    return int(sratios_byte.hex(), 16)



def main():

    #ret = balanceOf(ea, const.contract_CFToken_usdc[ea.host], '0xe352dfb9518a9616719232cf53fd2e32a3864305')
    #ret = totalSupply(ea, const.contract_CFVault[ea.host])

    # print(ea.get_tx_receipt(
    #     '0xd9bf87c5e1bcf1635ec79ef726bef291def5de2825ad1348c9a710bcdff6a4c1'))

    #print(ea.getGasPrice())
    print(ea.get_deposit_to('0x346a502e29f0d317e5b97d3bbb6ecb2977de36ff785e86336ac74690ccbb329a'))

    # ret = decimals(ea, const.contract_HGateKeeper[ea.host])
    # ret = getPricePerFullShare(ea, const.contract_HGateKeeper[ea.host])
    # ret = underlying_balance(ea, const.contract_HGateKeeper[ea.host])


    # ret = getDecimal(ea, const.contract_YieldStream[ea.host])
    # ret = getCurrentPeriod(ea, const.contract_HAuctionHouse[ea.host])
    # ret = getCurrentPeriodStartBlock(ea, const.contract_HAuctionHouse[ea.host])
    # ret = balance(ea, const.contract_HGateKeeper[ea.host])
    # ret = getParamPeriodBlockNum(ea, const.contract_HAuctionHouse[ea.host])
    # ret = sratios(ea, const.contract_HAuctionHouse[ea.host], 0)
    # print(ret)


if __name__ == '__main__':
    main()
