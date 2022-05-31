<script>
import {
  getIERCBalanceOf,
  getETHBalance,
  getAllowance,
  setDeposit,
  setDepositETH,
  getWithdraw,
  setApprove,
} from '@/common/web3'

import { getAsset, getProfit } from '@/common/api'
import {
  dividedBy,
  setConfirmValue,
  setWithdrawValue,
  isLessThanOrEqualTo,
  setAssetsValue,
  random,
  multipliedByFixed,
  isLt,
  minusLet,
  minus,
} from '@/utils'
import { Contract, TTIMER, LMarkets } from '../../config.js'
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState(['MetaMaskAddress', 'Pendings']),
  },
  props: {
    goData: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      list: [],
      marks: {
        0: '0',
        25: '25%',
        50: '50%',
        75: '75%',
        100: '100%',
      },
      textList: {
        USDC: 'Invest in stable-coin pools based on Convex / Curve, rewards received will be converted into corresponding asset for further investment automatically.',
        WBTC: 'Invest in BTC pools based on Convex / Curve, rewards received will be converted into corresponding asset for further investment automatically.',
        ETH: 'Invest in ETH pools based on Convex / Curve, rewards received will be converted into corresponding asset for further investment automatically.',
      },
      loading: null,
      itemData: null,
      Max: 0,
      totalOf: 0,
      withdrawInput: 0,
      withdrawVal: 0,
      confirmInput: 0,
      confirmVal: 0,
      dialogVisible: false,
      title: '',
      diaWidth: '40%',
      dialogName: '',
      echartsData: [],
      tableData: [],
      isApprove: true,
      ratio: '0%',
      codeurl: '',
    }
  },
  watch: {
    Pendings(cur, old) {
      if (old.length > cur.length) {
        if (!this.itemData) return
        this.getTotalOf(this.itemData.code)
      }
    },
    MetaMaskAddress(cur, old) {
      this.getAssetList()
    },
  },
  mounted() {
    this.getAssetList()
  },
  methods: {
    getTimer() {
      LMarkets.forEach((item) => {
        const timer = random(TTIMER[0], TTIMER[1])
        this[item + 'timer'] = setInterval(() => {
          this.getAssets(item)
        }, timer)
      })
    },
    async getAssets(codename) {
      const usdcData = await getAsset(this.MetaMaskAddress, codename)
      const list = [...this.list]
      list.forEach((item, idx) => {
        if (
          item.code === usdcData.data.code &&
          item.totalassets !== usdcData.data.totalassets
        ) {
          const showContent = this.itemData ? this.itemData.showContent : false
          const obj = { ...usdcData.data, showContent: showContent }
          this.itemData = this.itemData ? { ...obj } : null
          this.$set(this.list, idx, { ...obj })
        }
      })
    },
    async getAssetList() {
      this.isLoading()
      Promise.all(
        LMarkets.map((item, idx) => {
          return getAsset(this.MetaMaskAddress, item)
        })
      )
        .then(([...LMarkets]) => {
          this.list = LMarkets.map((item) => {
            return {
              ...item.data,
              showContent: false,
            }
          })
          if (this.$route.params.type && this.$route.params.type === 'low') {
            const data = this.list.find(
              (item) => item.code === this.$route.params.code
            )
            this.changeContent(data)
          }
          LMarkets.forEach((item) => {
            clearInterval(this[item + 'timer'])
            this[item + 'timer'] = null
          })
          this.getTimer()
          this.downLoading()
        })
        .catch((err) => {
          this.downLoading()
          console.log(err, '=-')
        })
    },

    async approve() {
      if (!this.MetaMaskAddress) return this.Warning('Please link wallet')
      this.isLoading()
      try {
        const resApprove = await setApprove(
          new BigNumber(1e32).toString(10),
          this.MetaMaskAddress,
          this.itemData.code
        )
        if (resApprove.status) {
          this.isApprove = false
          this.Success('Successfully authorized.')
          this.downLoading()
        }
      } catch (error) {
        this.downLoading()
      }
    },
    async confirm(item) {
      if (!this.MetaMaskAddress) return this.Warning('Please link wallet')
      if (Number(this.confirmInput) === 0) return this.Warning('Invalid Value')
      const less = isLessThanOrEqualTo(this.confirmInput, this.totalOf)
      if (!less) return this.Warning('Invalid Value')
      if (item.code === 'ETH') {
        const minNum = isLt(this.confirmInput, 0.01)
        if (minNum) return this.Warning('Minimum deposit amount 0.01 ETH.')
        const maxNum = minusLet(this.confirmInput, this.totalOf)
        if (!maxNum)
          return this.Warning(
            'The amount of asset you want to deposit exceeds the safe max value, which may lead to failure to pay gas fee.',
            'Invalid value'
          )
      }
      const decimal = Contract[item.code].Decimal
      const bigInput = setConfirmValue(this.confirmInput, decimal)
      const params =
        this.itemData.code === 'ETH'
          ? await setDepositETH(
              bigInput,
              this.MetaMaskAddress,
              this.itemData.code,
              'low'
            )
          : await setDeposit(bigInput, this.MetaMaskAddress, this.itemData.code)
      this.sendTransaction(params)
    },
    withdrawItem(item) {
      if (!this.MetaMaskAddress) return this.Warning('Please link wallet')
      if (Number(this.withdrawInput) === 0) return this.Warning('Invalid Value')
      const less = isLessThanOrEqualTo(this.withdrawInput, item.user_assets)
      if (!less) return this.Warning('Invalid Value')
      this.withdraw(item)
    },
    async withdraw(item) {
      const maxWithdraw = this.withdrawInput === item.user_assets
      const bigInput =
        maxWithdraw === true
          ? item.lp_token
          : setWithdrawValue(
              this.withdrawInput,
              item.lp_token,
              item.user_assets
            )
      const params = await getWithdraw(
        bigInput,
        this.MetaMaskAddress,
        item.code
      )
      this.sendTransaction(params)
    },
    inputConfirm() {
      this.confirmVal = 0
    },
    setConfirmVal(item) {
      const num =
        this.itemData.code === 'ETH' ? minus(this.totalOf) : this.totalOf
      this.confirmInput = setAssetsValue(item, num)
    },
    setWithdrawVal(item) {
      this.withdrawInput =
        item === 100
          ? this.itemData.user_assets
          : setAssetsValue(item, this.itemData.user_assets)
      this.inputWithdraw('set')
    },
    inputWithdraw(type = null) {
      if (type !== 'set') {
        this.withdrawVal = 0
        console.log(type)
      }
      if (!this.withdrawInput) {
        this.ratio = Number(this.itemData.ratio) * 100 + '%'
        return
      }
      if (Number(this.withdrawInput) === 0) {
        this.ratio = Number(this.itemData.ratio) * 100 + '%'
        return
      }
      this.ratio = multipliedByFixed(
        this.withdrawInput,
        this.itemData.ratio,
        Contract[this.itemData.code].Length
      )
    },
    setMax(type, val) {
      if (type === 1) {
        this.confirmInput = this.itemData.code === 'ETH' ? minus(val) : val
      } else {
        this.withdrawInput = val.user_assets
        this.inputWithdraw()
      }
    },
    isLoading() {
      this.loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)',
      })
    },
    downLoading() {
      if (this.loading) {
        this.loading.close()
      }
      this.loading = null
    },
    async changeContent(val) {
      this.isLoading()
      this.withdrawInput = 0
      this.withdrawVal = 0
      this.confirmInput = 0
      this.confirmVal = 0
      this.isApprove = true
      if (val.code !== 'ETH' && !val.showContent && this.MetaMaskAddress) {
        const allowance = await getAllowance(this.MetaMaskAddress, val.code)
        const myAllowance = dividedBy(allowance, Contract[val.code].Decimal)
        const less = isLessThanOrEqualTo(myAllowance, 0)
        this.isApprove = less
      }
      this.list.map((item) => {
        if (val.code === item.code) {
          item.showContent = !item.showContent
          if (item.showContent) {
            this.itemData = { ...val }
            this.ratio = Number(val.ratio) * 100 + '%'
            this.downLoading()
            this.getTotalOf(val.code)
          } else {
            this.downLoading()
            this.itemData = null
          }
        } else {
          item.showContent = false
        }
      })
    },

    async getTotalOf(code) {
      if (!this.MetaMaskAddress) {
        this.totalOf = 0
        return this.downLoading()
      }
      const bcf =
        code === 'ETH'
          ? await getETHBalance(this.MetaMaskAddress)
          : await getIERCBalanceOf(this.MetaMaskAddress, code)
      const number = Contract[code].Decimal
      this.totalOf = dividedBy(bcf, number)
      try {
      } catch (error) {}
    },
    closeMain(val) {
      this.title = ''
      this.dialogVisible = val
    },

    async selectLine() {
      this.codeurl = this.itemData.code.toLowerCase()
      const list = await getProfit(this.codeurl)
      this.echartsData = list.dataList
      this.title = '7 Days APY'
      this.dialogName = 'EchartsLine'
      this.diaWidth = '80%'
      this.dialogVisible = true
    },
    async selectTable() {
      this.codeurl = this.itemData.code.toLowerCase()
      this.title = 'History'
      this.dialogName = 'CffTable'
      this.diaWidth = '80%'
      this.dialogVisible = true
    },
  },

  destroyed() {
    LMarkets.forEach((item) => {
      clearInterval(this[item + 'timer'])
      this[item + 'timer'] = null
    })
  },
}
</script>
