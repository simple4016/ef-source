
import web3
import json
import sys
import util


class contract_base:

    def __init__(self, w3, compiled_path):
        assert isinstance(w3, web3.main.Web3)
        assert isinstance(compiled_path, str)
        self.w3 = w3
        self.compiled_home = compiled_path


    def __build_transaction(self, args):
        assert isinstance(args.sender, str)
        assert isinstance(args.gas_limit, int)
        assert isinstance(args.tx_value, int)
        transaction = {
            'from': args.sender,
            'nonce': self.w3.eth.getTransactionCount(args.sender),
            'value': args.tx_value,
            'gas': args.gas_limit,
            'gasPrice': self.w3.toWei('10', 'gwei')
        }
        return transaction


    def __construct(self, transaction, args):
        assert isinstance(transaction, dict)

        contract_name = args.contract_name
        func_args = args.func_args
        assert isinstance(contract_name, str)
        assert isinstance(func_args, list)
        print(func_args)

        abi_path = '%s/%s_abi.json' % (self.compiled_home, contract_name)
        bytecode_path = '%s/%s_bytecode.json' % (self.compiled_home, contract_name)

        contract = util.construct_from_abi_and_bytecode(self.w3, abi_path, bytecode_path)
        construct_tx = contract.constructor(*func_args).buildTransaction(transaction)
        return construct_tx


    def deploy_contract(self, args):
        transaction = self.__build_transaction(args)
        construct_tx = self.__construct(transaction, args)
        construct_tx['to'] = construct_tx['to'].hex()
        return json.dumps(construct_tx)


    def __call(self, contract, transaction, func_name, args):
        assert isinstance(contract, web3.contract.Contract)
        assert isinstance(transaction, dict)
        assert isinstance(func_name, str)
        assert isinstance(args, list)
        print(args)

        call_tx = eval('contract.functions.%s(*args).buildTransaction(transaction)' % func_name)
        ret = eval('contract.functions.%s(*args).call(transaction)' % func_name)
        print(ret)
        return call_tx


    def call_contract(self, args):
        assert isinstance(args.contract_address, str)
        assert isinstance(args.contract_name, str)
        assert isinstance(args.func_name, str)
        assert isinstance(args.func_args, list)
        transaction = self.__build_transaction(args)

        abi_path = '%s/%s_abi.json' % (self.compiled_home, args.contract_name)
        contract = util.construct_from_abi_and_address(self.w3, abi_path, args.contract_address)

        call_tx = self.__call(contract, transaction, args.func_name, args.func_args)
        return json.dumps(call_tx)


