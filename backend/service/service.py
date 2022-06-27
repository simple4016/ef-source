import sys
import pytz
sys.path.append('../common')  # noqa:E402

from db_tables import UserLogs
from db_tables import db
from db_tables import PriceLogs
from db_tables import ProfitLogs
from db_tables import TransferLogs
from db_tables import TokenProfile_usdc
from db_tables import PriceHistory
from db_tables import GasPrice

from db_tables import PriceLogsWbtc
from db_tables import ProfitLogsWbtc
from db_tables import TransferLogsWbtc
from db_tables import UserLogsWbtc

from db_tables import TokenProfile_wbtc

from db_tables import PriceHistoryWbtc



from db_tables import PriceLogsEth
from db_tables import ProfitLogsEth
from db_tables import TransferLogsEth
from db_tables import UserLogsEth

from db_tables import TokenProfile_eth

from db_tables import PriceHistoryEth
import const
import json


def __calculate_sevenday_apy_usdc(day, item_numbers):

    query = db.session.query(
        ProfitLogs.profit_ratio).filter(ProfitLogs.pub_date <= day).order_by(
            ProfitLogs.pub_date.desc()).limit(item_numbers).all()

    ratioes = []
    for item in query:
        ratioes.append(item.profit_ratio)
    return sum(ratioes), len(query)




def __calculate_sevenday_apy_wbtc(day, item_numbers):

    query = db.session.query(ProfitLogsWbtc.profit_ratio).filter(
        ProfitLogsWbtc.pub_date <= day).order_by(
            ProfitLogsWbtc.pub_date.desc()).limit(item_numbers).all()
    ratioes = []
    for item in query:
        ratioes.append(item.profit_ratio)
    return sum(ratioes), len(query)


def __calculate_sevenday_apy_eth(day, item_numbers):

    query = db.session.query(ProfitLogsEth.profit_ratio).filter(
        ProfitLogsEth.pub_date <= day).order_by(
            ProfitLogsEth.pub_date.desc()).limit(item_numbers).all()
    ratioes = []
    for item in query:
        ratioes.append(item.profit_ratio)
    return sum(ratioes), len(query)


def get_Gas(params):
    info = db.session.query(GasPrice).all()
    if not info:
        return json.dumps({'gasprice':60})
    assert len(info) == 1
    newGasPrice = info[0]
    gas_price_new = int(newGasPrice.gas_price)

    return json.dumps({'gasprice':gas_price_new})

def get_Asset(params):
    usdc_amount_p_usdc, cff_amount_user_usdc,current_profit_usdc,logs_all_usdc = get_PrivateAsset_USDC(params)
    usdc_amount_p_eth, cff_amount_user_eth,current_profit_eth,logs_all_eth = get_PrivateAsset_ETH(params)
    usdc_amount_p_wbtc, cff_amount_user_wbtc,current_profit_wbtc,logs_all_wbtc = get_PrivateAsset_WBTC(params)

    info = db.session.query(PriceLogs).order_by(
        PriceLogs.pub_date.desc()).limit(1).all()
    if not info:
        return;
    assert len(info) == 1
    priceLog = info[0]
    totalS = int(priceLog.cff_amount)
    virtual_p = int(priceLog.virtual_price)

    ret = ((totalS / float(10**const.PARAMS_CFT_DECIMAL)))

    ret = ret * (virtual_p / float(10**const.PARAMS_CFT_DECIMAL))
    total_asset = ret

    query = db.session.query(UserLogs).all()

    for item in query:
        if item.operation_type == '0':

            ret -= (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))
        else:
            ret += (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))

    total_profit = ret

    # this is for wbtc

    info_wbtc = db.session.query(PriceLogsWbtc).order_by(
        PriceLogsWbtc.pub_date.desc()).limit(1).all()
    if not info_wbtc :
        return ;

    assert len(info_wbtc) == 1

    priceLog_wbtc = info_wbtc[0]
    totalS_wbtc = int(priceLog_wbtc.cff_amount)
    virtual_p_wbtc = int(priceLog_wbtc.virtual_price)

    ret_wbtc = ((totalS_wbtc / float(10**const.PARAMS_CFT_DECIMAL)))

    ret_wbtc = ret_wbtc * (virtual_p_wbtc /
                           float(10**const.PARAMS_CFT_DECIMAL))
    total_asset_wbtc = ret_wbtc

    query = db.session.query(UserLogsWbtc).all()

    for item in query:
        if item.operation_type == '0':

            ret_wbtc -= (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))
        else:
            ret_wbtc += (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))

    total_profit_wbtc = ret_wbtc


        # this is for eth

    info_eth = db.session.query(PriceLogsEth).order_by(
        PriceLogsEth.pub_date.desc()).limit(1).all()
    if not info_eth :
        return ;

    assert len(info_eth) == 1

    priceLog_eth = info_eth[0]
    totalS_eth = int(priceLog_eth.cff_amount)
    virtual_p_eth = int(priceLog_eth.virtual_price)

    ret_eth = ((totalS_eth / float(10**const.PARAMS_CFT_DECIMAL)))

    ret_eth = ret_eth * (virtual_p_eth /
                           float(10**const.PARAMS_CFT_DECIMAL))
    total_asset_eth = ret_eth

    query = db.session.query(UserLogsEth).all()

    for item in query:
        if item.operation_type == '0':

            ret_eth -= (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))
        else:
            ret_eth += (int(item.cff_amount)/float(10**const.PARAMS_CFT_DECIMAL)) * \
                (int(item.virtual_price)/float(10**const.PARAMS_CFT_DECIMAL))

    total_profit_eth = ret_eth


    info = db.session.query(PriceHistory).order_by(
        PriceHistory.pub_date.desc()).limit(1).all()

    if not info:
        return json.dumps([
             {
        'code': 'USDC',
        'totalassets': total_asset,
        'totalprofit': total_profit,
        'yesterdayProfit': 0,
        'sevendayProfit': float(("%.5f" % 0)),
        'profitVary': [],
                    'user_assets': cff_amount_user_usdc,
            'user_profit': current_profit_usdc,
            'logs_user': logs_all_usdc
    },
            {
        'code': 'WBTC',
        'totalassets': total_asset_wbtc,
        'totalprofit': total_profit_wbtc,
            'yesterdayProfit': 0,
        'sevendayProfit': float("%.5f" % 0),
            'profitVary': [],
            'user_assets': cff_amount_user_wbtc,
            'user_profit': current_profit_wbtc,
            'logs_user': logs_all_wbtc
    },{
        'code': 'ETH',
        'totalassets': total_asset_eth,
        'totalprofit': total_profit_eth,
        'yesterdayProfit': 0,
        'sevendayProfit': float(("%.5f" % 0)),
        'profitVary': [],
                            'user_assets': cff_amount_user_eth,
            'user_profit': current_profit_eth,
            'logs_user': logs_all_eth

    }
                           ]);

    assert len(info) == 1

    price_history_item = info[0]
    virtual_p_yes = int(price_history_item.virtual_price)
    cff_amount_yes = int(price_history_item.cff_amount)
    pub_date_yes = price_history_item.pub_date
    if virtual_p_yes == 0:
        yes_profit_ratio = 0
    else:
        yes_profit_ratio = (virtual_p - virtual_p_yes) / float(virtual_p_yes)





    yes_profit_ratio = yes_profit_ratio * 365

    sum_ratio, len_days = __calculate_sevenday_apy_usdc(
        int(pub_date_yes) + int(86400), 9)
    yes_profit_ratio = (sum_ratio * 365 + yes_profit_ratio) / (len_days + 1)

    yes_profit_ratio = int(yes_profit_ratio * 10000)
    yes_profit_ratio = float(yes_profit_ratio / float(10000))
    yes_profit_ratio = 0 if yes_profit_ratio < 0 else yes_profit_ratio

    yes_profit = int(virtual_p) * (int(totalS)) / float(
        10**(2 * const.PARAMS_CFT_DECIMAL))
    yes_profit -= int(virtual_p_yes) * (int(cff_amount_yes)) / float(
        10**(2 * const.PARAMS_CFT_DECIMAL))

    query = db.session.query(UserLogs).filter(
        UserLogs.pub_date > (int(pub_date_yes) + int(86400)))

    for item in query:
        if item.operation_type == '0':
            yes_profit -= (int(item.cff_amount) * (int(item.virtual_price)) /
                           float(10**(2 * const.PARAMS_CFT_DECIMAL)))

        else:
            yes_profit += (int(item.cff_amount) * (int(item.virtual_price)) /
                           float(10**(2 * const.PARAMS_CFT_DECIMAL)))

    query = db.session.query(ProfitLogs).order_by(
        ProfitLogs.pub_date.desc()).limit(30).all()

    unsorteda_new = []
    unsorteda_new.append({
        'date': (int(pub_date_yes) + int(86400)),
        'profit': yes_profit_ratio
    })

    for item in query:
        # current_profit -= int(item.cff_amount) * int(item.virtual_price)
        query_new, number_query = __calculate_sevenday_apy_usdc(
            item.pub_date, 10)

        unsorteda_new.append({
            'date': item.pub_date,
            'profit': float(query_new) * 365 / (number_query)
        })

    sortedArray = sorted(unsorteda_new, key=lambda x: x['date'], reverse=False)

# this is for wbtc
    info = db.session.query(PriceHistoryWbtc).order_by(
        PriceHistoryWbtc.pub_date.desc()).limit(1).all()
    if not info:
        return json.dumps([
             {
        'code': 'USDC',
        'totalassets': total_asset,
        'totalprofit': total_profit,
        'yesterdayProfit': yes_profit,
        'sevendayProfit': float(("%.5f" % yes_profit_ratio)),
        'profitVary': sortedArray,
                    'user_assets': cff_amount_user_usdc,
            'user_profit': current_profit_usdc,
            'logs_user': logs_all_usdc
    },{
        'code': 'WBTC',
        'totalassets': total_asset_wbtc,
        'totalprofit': total_profit_wbtc,
            'yesterdayProfit': 0,
        'sevendayProfit': float("%.5f" % 0),
            'profitVary': [],
                        'user_assets': cff_amount_user_wbtc,
            'user_profit': current_profit_wbtc,
            'logs_user': logs_all_wbtc

    },{
        'code': 'ETH',
        'totalassets': total_asset_eth,
        'totalprofit': total_profit_eth,
        'yesterdayProfit': 0,
        'sevendayProfit': float(("%.5f" % 0)),
        'profitVary': [],
                    'user_assets': cff_amount_user_eth,
            'user_profit': current_profit_eth,
            'logs_user': logs_all_eth
    }]);

    assert len(info) == 1

    price_history_item_wbtc = info[0]
    virtual_p_yes_wbtc = int(price_history_item_wbtc.virtual_price)
    cff_amount_yes_wbtc = int(price_history_item_wbtc.cff_amount)
    pub_date_yes_wbtc = price_history_item_wbtc.pub_date
    if virtual_p_yes_wbtc ==0:
        yes_profit_ratio_wbtc =0
    else:
        yes_profit_ratio_wbtc = (virtual_p_wbtc -
                             virtual_p_yes_wbtc) / float(virtual_p_yes_wbtc)
    yes_profit_ratio_wbtc = yes_profit_ratio_wbtc * 365

    sum_ratio, len_days = __calculate_sevenday_apy_wbtc(
        int(pub_date_yes_wbtc) + int(86400), 9)
    yes_profit_ratio_wbtc = (sum_ratio * 365 +
                             yes_profit_ratio_wbtc) / (len_days + 1)
    yes_profit_ratio_wbtc = int(yes_profit_ratio_wbtc * 10000)
    yes_profit_ratio_wbtc = float(yes_profit_ratio_wbtc / float(10000))
    yes_profit_ratio_wbtc = 0 if yes_profit_ratio_wbtc < 0 else yes_profit_ratio_wbtc

    yes_profit_wbtc = int(virtual_p_wbtc) * (int(totalS_wbtc)) / float(
        10**(2 * const.PARAMS_CFT_DECIMAL))
    yes_profit_wbtc -= int(virtual_p_yes_wbtc) * (
        int(cff_amount_yes_wbtc)) / float(10**(2 * const.PARAMS_CFT_DECIMAL))


    query = db.session.query(UserLogsWbtc).filter(
        UserLogsWbtc.pub_date > (int(pub_date_yes_wbtc) + int(86400)))

    for item in query:
        if item.operation_type == '0':
            yes_profit_wbtc -= (int(item.cff_amount) *
                                (int(item.virtual_price)) /
                                float(10**(2 * const.PARAMS_CFT_DECIMAL)))

        else:
            yes_profit_wbtc += (int(item.cff_amount) *
                                (int(item.virtual_price)) /
                                float(10**(2 * const.PARAMS_CFT_DECIMAL)))

    query = db.session.query(ProfitLogsWbtc).order_by(
        ProfitLogsWbtc.pub_date.desc()).limit(30).all()

    unsorteda_new_wbtc = []
    unsorteda_new_wbtc.append({
        'date': (int(pub_date_yes_wbtc) + int(86400)),
        'profit': yes_profit_ratio_wbtc
    })

    for item in query:
        # current_profit -= int(item.cff_amount) * int(item.virtual_price)
        query_new, number_query = __calculate_sevenday_apy_wbtc(
            item.pub_date, 10)
        unsorteda_new_wbtc.append({
            'date':
            item.pub_date,
            'profit':
            float(query_new) * 365 / (number_query)
        })

    sortedArray_wbtc = sorted(unsorteda_new_wbtc,
                              key=lambda x: x['date'],
                              reverse=False)




    # this is for eth
    info = db.session.query(PriceHistoryEth).order_by(
        PriceHistoryEth.pub_date.desc()).limit(1).all()
    if not info:
        return json.dumps([
             {
        'code': 'USDC',
        'totalassets': total_asset,
        'totalprofit': total_profit,
        'yesterdayProfit': yes_profit,
        'sevendayProfit': float(("%.5f" % yes_profit_ratio)),
        'profitVary': sortedArray,
                    'user_assets': cff_amount_user_usdc,
            'user_profit': current_profit_usdc,
            'logs_user': logs_all_usdc
    },{
        'code': 'WBTC',
        'totalassets': total_asset_wbtc,
        'totalprofit': total_profit_wbtc,
            'yesterdayProfit': yes_profit_wbtc,
        'sevendayProfit': float("%.5f" % yes_profit_ratio_wbtc),
            'profitVary': sortedArray_wbtc,
                        'user_assets': cff_amount_user_wbtc,
            'user_profit': current_profit_wbtc,
            'logs_user': logs_all_wbtc
    },{
        'code': 'ETH',
        'totalassets': total_asset_eth,
        'totalprofit': total_profit_eth,
        'yesterdayProfit': 0,
        'sevendayProfit': float(("%.5f" % 0)),
        'profitVary': [],
        'user_assets': cff_amount_user_eth,
            'user_profit': current_profit_eth,
            'logs_user': logs_all_eth
    }]);

    assert len(info) == 1

    price_history_item_eth = info[0]
    virtual_p_yes_eth = int(price_history_item_eth.virtual_price)
    cff_amount_yes_eth = int(price_history_item_eth.cff_amount)
    pub_date_yes_eth = price_history_item_eth.pub_date
    if virtual_p_yes_eth ==0:
        yes_profit_ratio_eth =0
    else:
        yes_profit_ratio_eth = (virtual_p_eth -
                             virtual_p_yes_eth) / float(virtual_p_yes_eth)
    yes_profit_ratio_eth = yes_profit_ratio_eth * 365

    sum_ratio, len_days = __calculate_sevenday_apy_eth(
        int(pub_date_yes_eth) + int(86400), 9)
    yes_profit_ratio_eth = (sum_ratio * 365 +
                             yes_profit_ratio_eth) / (len_days + 1)
    yes_profit_ratio_eth = int(yes_profit_ratio_eth * 10000)
    yes_profit_ratio_eth = float(yes_profit_ratio_eth / float(10000))
    yes_profit_ratio_eth = 0 if yes_profit_ratio_eth < 0 else yes_profit_ratio_eth

    yes_profit_eth = int(virtual_p_eth) * (int(totalS_eth)) / float(
        10**(2 * const.PARAMS_CFT_DECIMAL))
    yes_profit_eth -= int(virtual_p_yes_eth) * (
        int(cff_amount_yes_eth)) / float(10**(2 * const.PARAMS_CFT_DECIMAL))


    query = db.session.query(UserLogsEth).filter(
        UserLogsEth.pub_date > (int(pub_date_yes_eth) + int(86400)))

    for item in query:
        if item.operation_type == '0':
            yes_profit_eth -= (int(item.cff_amount) *
                                (int(item.virtual_price)) /
                                float(10**(2 * const.PARAMS_CFT_DECIMAL)))

        else:
            yes_profit_eth += (int(item.cff_amount) *
                                (int(item.virtual_price)) /
                                float(10**(2 * const.PARAMS_CFT_DECIMAL)))

    query = db.session.query(ProfitLogsEth).order_by(
        ProfitLogsEth.pub_date.desc()).limit(30).all()

    unsorteda_new_eth = []
    unsorteda_new_eth.append({
        'date': (int(pub_date_yes_eth) + int(86400)),
        'profit': yes_profit_ratio_eth
    })

    for item in query:
        # current_profit -= int(item.cff_amount) * int(item.virtual_price)
        query_new, number_query = __calculate_sevenday_apy_eth(
            item.pub_date, 10)
        unsorteda_new_eth.append({
            'date':
            item.pub_date,
            'profit':
            float(query_new) * 365 / (number_query)
        })

    sortedArray_eth = sorted(unsorteda_new_eth,
                              key=lambda x: x['date'],
                              reverse=False)


    return json.dumps([{
        'code': 'USDC',
        'totalassets': total_asset,
        'totalprofit': total_profit,
        'yesterdayProfit': yes_profit,
        'sevendayProfit': float(("%.5f" % yes_profit_ratio)),
        'profitVary': sortedArray,
        'user_assets': cff_amount_user_usdc,
            'user_profit': current_profit_usdc,
            'logs_user': logs_all_usdc
        },{
        'code': 'WBTC',
        'totalassets': total_asset_wbtc,
        'totalprofit': total_profit_wbtc,
        'yesterdayProfit': yes_profit_wbtc,
        'sevendayProfit': float("%.5f" % yes_profit_ratio_wbtc),
        'profitVary': sortedArray_wbtc,
                    'user_assets': cff_amount_user_wbtc,
            'user_profit': current_profit_wbtc,
            'logs_user': logs_all_wbtc
        },{
        'code': 'ETH',
        'totalassets': total_asset_eth,
        'totalprofit': total_profit_eth,
        'yesterdayProfit': yes_profit_eth,
        'sevendayProfit': float(("%.5f" % yes_profit_ratio_eth)),
            'profitVary': sortedArray_eth,
                        'user_assets': cff_amount_user_eth,
            'user_profit': current_profit_eth,
            'logs_user': logs_all_eth
        }                       ])

def get_PrivateAsset_USDC(params):
    current_profit = 0
    usdc_amount_p = 0.0
    cff_amount_user = 0.0


    logs_all = []
    if 'address' not in params:
        return usdc_amount_p, cff_amount_user,current_profit,logs_all

    address = params['address'][2:].lower()


    query = db.session.query(TokenProfile_usdc).filter(
        TokenProfile_usdc.address == address).all()
    if not query:
        return usdc_amount_p, cff_amount_user,current_profit,logs_all

        # return json.dumps({
        #     'totalassets': usdc_amount_p,
        #     'totalprofit': current_profit,
        #     'logs_user': logs_all
        # })
    else:
        assert (len(query) == 1)
        queryitem = query[0]
        cff_amount_p = queryitem.amount

        info = db.session.query(PriceLogs).order_by(
            PriceLogs.pub_date.desc()).limit(1).all()

        assert len(info) == 1

        priceLog = info[0]

        virtual_p = int(priceLog.virtual_price)

        usdc_amount_p = int(virtual_p) * int(cff_amount_p) / (float(
            10**(2 * const.PARAMS_CFT_DECIMAL)))
        cff_amount_user = usdc_amount_p
        current_profit = usdc_amount_p

        query = db.session.query(UserLogs).filter(
            (UserLogs.address == address)).order_by(
                UserLogs.pub_date.desc()).all()
        usdc_amount_p_new = 0.0

        for item in query:
            if item.operation_type == '0':

                current_profit -= (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new += (int(item.usdc_amount) /
                                      float(10**const.PARAMS_USDC_DECIMAL))

                usdc_amount_p_new -= (int(item.usdc_fee) /
                                      float(10**const.PARAMS_USDC_DECIMAL))


                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    int(item.usdc_amount) /
                    float(10**const.PARAMS_USDC_DECIMAL),
                    'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_USDC_DECIMAL),
                    'operation':
                    '存入',
                    'flag':
                    'succes'
                })
            else:

                current_profit += (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new -= (
                    (int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_USDC_DECIMAL))


                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    (int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_USDC_DECIMAL),
                    'operation':
                    '取出',
                    'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_USDC_DECIMAL),
                    'flag':
                    'succes'
                })
        query = db.session.query(TransferLogs).filter(
            (TransferLogs.from_address == address)).order_by(
                TransferLogs.pub_date.desc()).all()
        for item in query:
            logs_all.append({
                'date':
                item.pub_date,
                'txh':
                '0x%s' % item.hash,
                'amount':
                int(item.cff_amount) / float(10**const.PARAMS_CFT_DECIMAL),
                'fee':
                0,
                'operation':
                '转出',
                'flag':
                'succes'
            })
        query = db.session.query(TransferLogs).filter(
            (TransferLogs.to_address == address)).order_by(
                TransferLogs.pub_date.desc()).all()
        for item in query:
            logs_all.append({
                'date':
                item.pub_date,
                'txh':
                '0x%s' % item.hash,
                'amount':
                int(item.cff_amount) / float(10**const.PARAMS_CFT_DECIMAL),
                'fee':
                0,
                'operation':
                '转入',
                'flag':
                'succes'
            })
        return usdc_amount_p_new, cff_amount_user,current_profit,logs_all
    # json.dumps({
    #         'totalassets': usdc_amount_p_new,
    #         'totalprofit': current_profit,
    #         'logs_user': logs_all
    #     })


def get_PrivateAsset_ETH(params):

    current_profit = 0
    usdc_amount_p = 0.0
    cff_amount_user = 0.0


    logs_all = []
    if 'address' not in params:
        return usdc_amount_p, cff_amount_user,current_profit,logs_all

    address = params['address'][2:].lower()











    query = db.session.query(TokenProfile_eth).filter(
        TokenProfile_eth.address == address).all()
    if not query:

        return usdc_amount_p,cff_amount_user,current_profit,logs_all

    else:
        assert (len(query) == 1)
        queryitem = query[0]
        cff_amount_p = queryitem.amount

        info = db.session.query(PriceLogsEth).order_by(
            PriceLogsEth.pub_date.desc()).limit(1).all()

        assert len(info) == 1

        priceLog = info[0]

        virtual_p = int(priceLog.virtual_price)

        usdc_amount_p = int(virtual_p) * int(cff_amount_p) / (float(
            10**(2 * const.PARAMS_CFT_DECIMAL)))
        current_profit = usdc_amount_p
        cff_amount_user = usdc_amount_p

        query = db.session.query(UserLogsEth).filter(
            (UserLogsEth.address == address)).order_by(
                UserLogsEth.pub_date.desc()).all()

        usdc_amount_p_new = 0.0
        for item in query:
            if item.operation_type == '0':
                current_profit -= (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new += (int(item.usdc_amount) /
                                      float(10**const.PARAMS_ETH_DECIMAL))

                usdc_amount_p_new -= (int(item.usdc_fee) /
                                      float(10**const.PARAMS_ETH_DECIMAL))

                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    int(item.usdc_amount) /
                    float(10**const.PARAMS_ETH_DECIMAL),
                    'operation':
                    '存入',
                    'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_ETH_DECIMAL),
                    'flag':
                    'succes'
                })
            else:

                current_profit += (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new -= (
                    (int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_ETH_DECIMAL))


                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    int(int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_ETH_DECIMAL),
                                            'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_ETH_DECIMAL),
                    'operation':
                    '取出',
                    'flag':
                    'succes'
                })
                query = db.session.query(TransferLogsEth).filter(
                    (TransferLogsEth.from_address == address)).order_by(
                        TransferLogsEth.pub_date.desc()).all()

                for item in query:
                    logs_all.append({
                        'date': item.pub_date,
                        'txh': '0x%s' % item.hash,
                        'amount': int(item.cff_amount) / float(10**18),
                        'operation': '转出',
                        'fee': 0,
                        'flag': 'succes'

                    })

                query = db.session.query(TransferLogsEth).filter(
                (TransferLogsEth.to_address == address)).order_by(
                    TransferLogsEth.pub_date.desc()).all()

                for item in query:

                    logs_all.append({
                        'date': item.pub_date,
                        'txh': '0x%s' % item.hash,
                        'amount': int(item.cff_amount) / float(10**18),
                        'operation': '转入',
                        'fee':0,
                        'flag': 'succes'
                    })

        return usdc_amount_p_new,cff_amount_user,current_profit,logs_all
        # return json.dumps({
        #     'totalassets': usdc_amount_p_new,
        #     'totalprofit': current_profit,
        #     'logs_user': logs_all
        # })

def get_PrivateAsset_WBTC(params):

    current_profit = 0
    usdc_amount_p = 0.0
    cff_amount_user = 0.0
    logs_all = []

    if 'address' not in params:
        return usdc_amount_p, cff_amount_user,current_profit,logs_all

    address = params['address'][2:].lower()

    query = db.session.query(TokenProfile_wbtc).filter(
        TokenProfile_wbtc.address == address).all()
    if not query:
        return usdc_amount_p,cff_amount_user,current_profit,logs_all

        # return json.dumps({
        #     'totalassets': usdc_amount_p,
        #     'totalprofit': current_profit,
        #     'logs_user': logs_all
        # })
    else:
        assert (len(query) == 1)
        queryitem = query[0]
        cff_amount_p = queryitem.amount

        info = db.session.query(PriceLogsWbtc).order_by(
            PriceLogsWbtc.pub_date.desc()).limit(1).all()

        assert len(info) == 1

        priceLog = info[0]

        virtual_p = int(priceLog.virtual_price)

        usdc_amount_p = int(virtual_p) * int(cff_amount_p) / (float(
            10**(2 * const.PARAMS_CFT_DECIMAL)))
        current_profit = usdc_amount_p
        cff_amount_user  = usdc_amount_p


        query = db.session.query(UserLogsWbtc).filter(
            (UserLogsWbtc.address == address)).order_by(
                UserLogsWbtc.pub_date.desc()).all()

        usdc_amount_p_new = 0.0
        for item in query:
            if item.operation_type == '0':
                current_profit -= (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new += (int(item.usdc_amount) /
                                      float(10**const.PARAMS_WBTC_DECIMAL))

                usdc_amount_p_new -= (int(item.usdc_fee) /
                                      float(10**const.PARAMS_WBTC_DECIMAL))

                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    int(item.usdc_amount) /
                    float(10**const.PARAMS_WBTC_DECIMAL),
                    'operation':
                    '存入',
                    'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_WBTC_DECIMAL),
                    'flag':
                    'succes'
                })
            else:

                current_profit += (
                    int(item.cff_amount) * (int(item.virtual_price)) /
                    float(10**(2 * const.PARAMS_CFT_DECIMAL)))

                usdc_amount_p_new -= (
                    (int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_WBTC_DECIMAL))


                logs_all.append({
                    'date':
                    item.pub_date,
                    'txh':
                    '0x%s' % item.hash,
                    'amount':
                    int(int(item.usdc_amount) + int(item.usdc_fee)) /
                    float(10**const.PARAMS_WBTC_DECIMAL),
                                            'fee':
                    int(item.usdc_fee) /
                    float(10**const.PARAMS_WBTC_DECIMAL),
                    'operation':
                    '取出',
                    'flag':
                    'succes'
                })
                query = db.session.query(TransferLogsWbtc).filter(
                    (TransferLogsWbtc.from_address == address)).order_by(
                        TransferLogsWbtc.pub_date.desc()).all()
        for item in query:
            logs_all.append({
                'date': item.pub_date,
                'txh': '0x%s' % item.hash,
                'amount': int(item.cff_amount) / float(10**18),
                'operation': '转出',
                'fee':0,
                'flag': 'succes'
            })
            query = db.session.query(TransferLogsWbtc).filter(
                (TransferLogsWbtc.to_address == address)).order_by(
                    TransferLogsWbtc.pub_date.desc()).all()
        for item in query:
            logs_all.append({
                'date': item.pub_date,
                'txh': '0x%s' % item.hash,
                'amount': int(item.cff_amount) / float(10**18),
                'operation': '转入',
                'fee':0,
                'flag': 'succes'
            })
        return usdc_amount_p_new,cff_amount_user,current_profit,logs_all
    # json.dumps({
    #         'totalassets': usdc_amount_p_new,
    #         'totalprofit': current_profit,
    #         'logs_user': logs_all
    #     })

def get_PrivateAsset(params):
    if 'address' not in params:
        return json.dumps({
            'error_code': 1,
            'error_message': 'must contain params address'
        })

    if 'code' not in params:
        return json.dumps({
            'error_code': 1,
            'error_message': 'must contain params code'
        })

    assert (params['code'] == 'USDC' or params['code'] == 'WBTC' or params['code'] == 'ETH')

    # if params['code'] == 'WBTC':

    # if params['code'] == 'USDC':

    # if params['code'] == 'ETH':
