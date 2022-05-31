<script>
import {
	getHIERCBalanceOf,
	setHDeposit,
	setDepositETH,
	getHWithdraw,
	getHAllowance,
	setHApprove,
	getETHBalance
} from '@/common/web3'
import { getAsset, getProfit } from '@/common/api'
import {
	dividedBy,
	setConfirmValue,
	setWithdrawValue,
	isLessThanOrEqualTo,
	setAssetsValue,
	random,
	isLt,
	minusLet,
	minus
} from '@/utils'
import { HContract, TTIMER, HMarkets } from '../../config'
import { mapState } from 'vuex'
export default {
	computed: {
		...mapState(['MetaMaskAddress', 'Pendings'])
	},
	data() {
		return {
			list: [],
			marks: {
				0: '0',
				25: '25%',
				50: '50%',
				75: '75%',
				100: '100%'
			},
			textList: {
				USDC: 'Invest in stable-coin pools based on Convex / Curve, rewards received will be converted into corresponding asset for further investment automatically.',
				WBTC: 'Invest in BTC pools based on Convex / Curve, rewards received will be converted into corresponding asset for further investment automatically.',
				ETH: 'Invest in steth using leverage to gain more interest, but with risk to be liquidated in extreme marketing conditions.'
			},
			loading: null,
			itemData: null,
			Max: 0,
			selectConfirm: 'USDC',
			selectWithdraw: 'USDC',
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
			isApprove: false,
			codeurl: '',
			isYield: false
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
		}
	},
	mounted() {
		this.getAssetList()
	},
	methods: {
		closeisYield() {
			this.isYield = false
		},
		selectWithdrawChange(val) {
			this.withdrawInput = 0
			this.withdrawVal = 0
		},
		selectConfirmChange(val) {
			this.getHAllowances(this.itemData)
			this.getTotalOf(this.itemData.code)
			this.confirmInput = 0
			this.confirmVal = 0
		},

		getTimer() {
			HMarkets.forEach((item) => {
				const timer = random(TTIMER[0], TTIMER[1])
				this['h' + item + 'timer'] = setInterval(() => {
					this.getAssets('h' + item)
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
		getAssetList() {
			this.isLoading()
			Promise.all(
				HMarkets.map((item) => {
					return getAsset(this.MetaMaskAddress, 'h' + item)
				})
			)
				.then(([...HMarkets]) => {
					this.list = HMarkets.map((item) => {
						return {
							...item.data,
							showContent: false
						}
					})
					if (this.$route.params.type && this.$route.params.type === 'high') {
						const data = this.list.find(
							(item) => item.code === this.$route.params.code
						)
						this.changeContent(data)
					}
					HMarkets.forEach((item) => {
						clearInterval(this['h' + item + 'timer'])
						this['h' + item + 'timer'] = null
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
				const resApprove = await setHApprove(
					new BigNumber(1e32).toString(10),
					this.MetaMaskAddress,
					this.itemData.code,
					this.selectConfirm
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
			const decimal = HContract[item.code]
			let bigInput = 0
			let params = null
			if (item.code === 'ETH') {
				bigInput = setConfirmValue(this.confirmInput, decimal.Decimal)
				params = await setDepositETH(
					bigInput,
					this.MetaMaskAddress,
					item.code,
					'high'
				)
			} else {
				bigInput = setConfirmValue(
					this.confirmInput,
					decimal[`${this.selectConfirm}Decimal`]
				)
				params = await setHDeposit(
					bigInput,
					this.MetaMaskAddress,
					item.code,
					this.selectConfirm
				)
			}
			this.sendTransaction(params)
		},
		withdrawItem(item) {
			if (!this.MetaMaskAddress) return this.Warning('Please link wallet')
			if (Number(this.withdrawInput) === 0) return this.Warning('Invalid Value')
			const user =
				this.selectWithdraw === 'USDC' ? 'user_assets' : 'user_assets_origin'
			const maxNum = item.code === 'ETH' ? item.user_assets : item[user]
			const less = isLessThanOrEqualTo(this.withdrawInput, maxNum)
			if (!less) return this.Warning('Invalid Value')
			if (isLt(item.user_profit, 0)) return (this.isYield = true)
			this.withdraw(item)
		},
		async withdraw(item) {
			this.isYield = false
			const user =
				this.selectWithdraw === 'USDC' ? 'user_assets' : 'user_assets_origin'
			const maxNum = item.code === 'ETH' ? item.user_assets : item[user]
			const maxWithdraw = this.withdrawInput === maxNum
			const bigInput = maxWithdraw
				? item.lp_token
				: setWithdrawValue(this.withdrawInput, item.lp_token, maxNum)
			const params = await getHWithdraw(
				bigInput,
				this.MetaMaskAddress,
				item.code,
				this.selectWithdraw
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
			if (this.itemData.code === 'ETH') {
				this.withdrawInput =
					item === 100
						? this.itemData.user_assets
						: setAssetsValue(item, this.itemData.user_assets)
			} else {
				const user =
					this.selectWithdraw === 'USDC' ? 'user_assets' : 'user_assets_origin'
				this.withdrawInput =
					item === 100
						? this.itemData[user]
						: setAssetsValue(item, this.itemData[user])
			}
		},
		inputWithdraw() {
			this.withdrawVal = 0
		},
		setMax(type, val) {
			if (type === 1) {
				this.confirmInput = this.itemData.code === 'ETH' ? minus(val) : val
			} else {
				const user =
					this.selectWithdraw === 'USDC' ? 'user_assets' : 'user_assets_origin'
				this.withdrawInput =
					this.itemData.code === 'ETH' ? val.user_assets : val[user]
			}
		},
		isLoading() {
			this.loading = this.$loading({
				lock: true,
				text: 'Loading',
				spinner: 'el-icon-loading',
				background: 'rgba(0, 0, 0, 0.7)'
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
				this.getHAllowances(val)
			}
			this.list.forEach((item) => {
				if (val.code === item.code) {
					item.showContent = !item.showContent
					if (item.showContent) {
						this.itemData = { ...val, showContent: item.showContent }
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
		async getHAllowances(val) {
			const allowance = await getHAllowance(
				this.MetaMaskAddress,
				val.code,
				this.selectConfirm
			)
			const myAllowance = dividedBy(
				allowance,
				HContract[val.code][`${this.selectConfirm}Decimal`]
			)
			console.log(myAllowance, 'myAllowance')
			const less = isLessThanOrEqualTo(myAllowance, 0)
			this.isApprove = less
		},
		async getTotalOf(code) {
			if (!this.MetaMaskAddress) {
				this.totalOf = 0
				return this.downLoading()
			}
			const bcf =
				code === 'ETH'
					? await getETHBalance(this.MetaMaskAddress)
					: await getHIERCBalanceOf(
							this.MetaMaskAddress,
							code,
							this.selectConfirm
					  )
			const number =
				code === 'ETH'
					? HContract[code].Decimal
					: HContract[code][`${this.selectConfirm}Decimal`]
			this.totalOf = dividedBy(bcf, number)
			this.downLoading()
			try {
			} catch (error) {}
		},
		closeMain(val) {
			this.title = ''
			this.dialogVisible = val
		},

		async selectLine() {
			this.codeurl = 'h' + this.itemData.code.toLowerCase()
			const list = await getProfit(this.codeurl)
			this.echartsData = list.dataList
			this.title = '7 Days APY'
			this.dialogName = 'EchartsLine'
			this.diaWidth = '80%'
			this.dialogVisible = true
		},
		async selectTable() {
			this.codeurl = 'h' + this.itemData.code.toLowerCase()
			this.title = 'History'
			this.dialogName = 'CffTable'
			this.diaWidth = '80%'
			this.dialogVisible = true
		}
	},
	destroyed() {
		HMarkets.forEach((item) => {
			clearInterval(this['h' + item + 'timer'])
			this[item + 'timer'] = null
		})
	}
}
</script>
