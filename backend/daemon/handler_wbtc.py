import sys
sys.path.append('../common')  # noqa:E402
from datetime import datetime, timezone
from eth_api import getVirtualPrice
from eth_api import totalSupply
from eth_api import split_by_32bytes
from eth_api import balanceOf

import const
from db_tables import TransferLogsWbtc
from db_tables import UserLogsWbtc
from db_tables import db
from db_tables import PriceLogsWbtc
from db_tables import ProfitLogsWbtc
from db_tables import TokenProfile_wbtc

from db_tables import PriceHistoryWbtc

import pytz

from sqlalchemy import func, text
from datetime import datetime, timedelta


def __update_price_Log_wbtc(ea):
    supply = totalSupply(ea, const.contract_CFToken_wbtc[ea.host])
    price = getVirtualPrice(ea, const.contract_CFVault_wbtc[ea.host])
    current_time = ea.get_block_time()  #
    price_log = PriceLogsWbtc(cff_amount=supply,
                              virtual_price=price,
                              pub_date=current_time)
    db.session.add(price_log)
    db.session.commit()


def __update_token_profile_wbtc(address, amount):

    query = db.session.query(TokenProfile_wbtc).filter(
        TokenProfile_wbtc.address == address).all()
    if not query:
        new_token_address = TokenProfile_wbtc(address=address, amount=amount)
        db.session.merge(new_token_address)
        db.session.commit()
    else:
        assert len(query) == 1
        new_token_address = TokenProfile_wbtc(id=query[0].id,
                                              address=address,
                                              amount=int(query[0].amount) +
                                              int(amount))
        db.session.merge(new_token_address)
        db.session.commit()


def calibrate_token_balance_wbtc(ea):
    query = db.session.query(TokenProfile_wbtc).all()
    for item in query:
        __update_token_profile_wbtc(
            item.address,
            int(
                balanceOf(ea, const.contract_CFToken_wbtc[ea.host],
                          '0x%s' % item.address)) - int(item.amount))


def initial_token_address_table_wbtc():

    query = db.session.query(UserLogsWbtc).filter(
        UserLogsWbtc.operation_type == 0).all()
    for item in query:
        __update_token_profile_wbtc(item.address, int(item.cff_amount))
    query = db.session.query(UserLogsWbtc).filter(
        UserLogsWbtc.operation_type == 1).all()
    for item in query:
        __update_token_profile_wbtc(item.address, -int(item.cff_amount))

    query = db.session.query(TransferLogsWbtc).all()
    for item in query:
        __update_token_profile_wbtc(item.from_address, -int(item.cff_amount))
        __update_token_profile_wbtc(item.to_address, int(item.cff_amount))


def timestamp_to_utcdate(timestamp1):
    return datetime.utcfromtimestamp(timestamp1)


def utcdate_to_timestamp(utctime):

    return utctime.replace(tzinfo=timezone.utc).timestamp()


def __handle_CUserdeposit_wbtc(data, txh, txtime, address_from):
    query = db.session.query(UserLogsWbtc).filter(
        UserLogsWbtc.hash == txh[2:]).all()
    if not query:
        chunks = split_by_32bytes(data[2:])
        assert len(chunks) == 4
        address = address_from

        usdc_amount = int(chunks[1], 16)
        cff_amount = int(chunks[2], 16)
        virtual_price = int(chunks[3], 16)
        userlogs = UserLogsWbtc(address=address,
                                hash=txh[2:],
                                usdc_amount = usdc_amount,
                                usdc_fee =0,
                                cff_amount=cff_amount,
                                virtual_price=virtual_price,
                                operation_type=0,
                                pub_date=txtime)
        db.session.merge(userlogs)
        db.session.commit()
        __update_token_profile_wbtc(address, int(cff_amount))



def __handle_CUserwithdraw_wbtc(data, txh, txtime):

    query = db.session.query(UserLogsWbtc).filter(
        UserLogsWbtc.hash == txh[2:]).all()

    if not query:

        chunks = split_by_32bytes(data[2:])
        assert len(chunks) == 5
        address = chunks[0][-40:]
        usdc_amount = int(chunks[1], 16)
        cff_amount = int(chunks[2], 16)
        usdc_fee = int(chunks[3], 16)
        virtual_price = int(chunks[4], 16)
        userlogs = UserLogsWbtc(address=address.lower(),
                                hash=txh[2:],
                                usdc_amount=usdc_amount,
                                cff_amount=cff_amount,
                                usdc_fee=usdc_fee,
                                virtual_price=virtual_price,
                                operation_type=1,
                                pub_date=txtime)
        db.session.merge(userlogs)
        db.session.commit()
        __update_token_profile_wbtc(address.lower(), -int(cff_amount))


def __handle_BidInfo_wbtc(change, txtime, ea):

    assert 'topics' in change
    topics = change['topics']
    assert topics
    event = topics[0].hex()
    assert 'data' in change
    data = change['data']
    transactionhash = change['transactionHash']

    if event == const.topic_CUserDeposit:
        deposit_address = ea.get_deposit_to(transactionhash.hex())


    if event == const.topic_CUserDeposit or event == const.topic_CUserDepositFee:

        __update_price_Log_wbtc(ea)

    if event == const.topic_CUserTransfer:

        from_address = change['topics'][1].hex()[-40:]

        to_address = change['topics'][2].hex()[-40:]

    op_code = {
        const.topic_CUserWithdraw:
        '__handle_CUserwithdraw_wbtc(data,transactionhash.hex(),txtime)',
        const.topic_CUserDeposit:
        '__handle_CUserdeposit_wbtc(data,transactionhash.hex(),txtime,deposit_address)',

        const.topic_CUserTransfer:
        '__handle_CUserTransfer_wbtc(data,transactionhash.hex(),txtime,from_address,to_address)'
    }
    eval(op_code[event])


def handle_BidInfo_wbtc(ea, bid_filter):

    changes = ea.get_filter_changes(bid_filter.filter_id)
    if changes:
        [
            __handle_BidInfo_wbtc(change, ea.get_block_time(), ea)
            for change in changes
        ]


def __handle_CUserTransfer_wbtc(data, transactionhash, txtime, from_address,
                                to_address):
    if (from_address != const.address_of_zero[2:]) and (to_address != const.address_of_zero[2:]) and (from_address !=const.contract_ERC20DepositApprover_wbtc[2:].lower()) and (to_address !=const.contract_ERC20DepositApprover_wbtc[2:].lower() ) and (from_address != const.contract_upgrade_wbtc[2:].lower()) and (to_address != const.contract_upgrade_wbtc[2:].lower()) :

        query = db.session.query(TransferLogsWbtc).filter(
            TransferLogsWbtc.hash == transactionhash[2:]).all()

        if not query:

            chunks = split_by_32bytes(data[2:])

            assert len(chunks) is 1

            cff_amount = int(chunks[0], 16)

            transferlogs = TransferLogsWbtc(from_address=from_address.lower(),
                                            to_address=to_address.lower(),
                                            hash=transactionhash[2:],
                                            cff_amount=cff_amount,
                                            pub_date=txtime)
            db.session.merge(transferlogs)
            db.session.commit()
            __update_token_profile_wbtc(from_address.lower(), -int(cff_amount))
            __update_token_profile_wbtc(to_address, int(cff_amount))


def handle_Supply_info_wbtc(ea):
    supply = totalSupply(ea, const.contract_CFToken_wbtc[ea.host])
    price = getVirtualPrice(ea, const.contract_CFVault_wbtc[ea.host])

    current_time = ea.get_block_time()  #
    #current_time = int(1609618853)

    info = db.session.query(PriceLogsWbtc).order_by(
        PriceLogsWbtc.pub_date.desc()).limit(1).all()
    if not info:
        price_log = PriceLogsWbtc(cff_amount=supply,
                                  virtual_price=price,
                                  pub_date=current_time)
        db.session.merge(price_log)
        db.session.commit()
        info = db.session.query(PriceLogsWbtc).order_by(
            PriceLogsWbtc.pub_date.desc()).limit(1).all()

    assert len(info) == 1
    priceLog = info[0]
    totalS = int(priceLog.cff_amount)
    virtual_p = int(priceLog.virtual_price)
    db_date = (priceLog.pub_date)

    if (timestamp_to_utcdate(db_date).day !=
            timestamp_to_utcdate(current_time).day):

        db_date_new = timestamp_to_utcdate(db_date)
        start_time_date = datetime(year=db_date_new.year,
                                   month=db_date_new.month,
                                   day=db_date_new.day,
                                   hour=0,
                                   minute=0,
                                   second=0)
        start_time_date = utcdate_to_timestamp(start_time_date)
        query = db.session.query(PriceHistoryWbtc).filter(
            PriceHistoryWbtc.pub_date == start_time_date).all()
        if not query:

            query = db.session.query(UserLogsWbtc).filter(
                UserLogsWbtc.pub_date < db_date).filter(
                    UserLogsWbtc.pub_date >= start_time_date).all()
            ret = 0
            for item in query:
                if item.operation_type == '0':
                    ret -= (int(item.cff_amount)/float(10**18)) *  \
                        (int(item.virtual_price)/(float(10**18)))
                else:
                    ret += (int(item.cff_amount)/float(10**18)) * \
                        (int(item.virtual_price)/(float(10**18)))
            ret += (int(totalS)/float(10**18)) *  \
                (int(virtual_p)/(float(10**18)))
            query = db.session.query(PriceHistoryWbtc).order_by(
                PriceHistoryWbtc.pub_date.desc()).limit(1).all()

            profit_ratio = 0
            if not query:
                ret -= 0
            else:

                price_history_item = query[0]
                if price_history_item.virtual_price ==0 :
                    ret -= 0
                    profit_ratio =0
                else:

                    ret -= (int(price_history_item.cff_amount)/float(10**18)) *  \
                    (int(price_history_item.virtual_price)/(float(10**18)))

                    if int(price_history_item.virtual_price) == 0:
                        profit_ratio =0;
                    else:


                        profit_ratio = (int(virtual_p) -
                                int(price_history_item.virtual_price)) / (int(
                                    price_history_item.virtual_price))

            price_history = PriceHistoryWbtc(cff_amount=totalS,
                                             virtual_price=virtual_p,
                                             pub_date=start_time_date)

            db.session.merge(price_history)

            db.session.commit()

            query = db.session.query(ProfitLogsWbtc).filter(
                ProfitLogsWbtc.pub_date == start_time_date).all()

            if not query:

                profit_ratio  =0 if profit_ratio < 0 else profit_ratio
                profitlog = ProfitLogsWbtc(profit_usdc=ret,
                                           profit_ratio=profit_ratio,
                                           pub_date=start_time_date)
                db.session.merge(profitlog)
                db.session.commit()

    price_log = PriceLogsWbtc(cff_amount=supply,
                              virtual_price=price,
                              pub_date=current_time)

    db.session.add(price_log)

    db.session.commit()
