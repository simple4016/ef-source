<script>
import Web3 from 'web3'
import Onboard from 'bnc-onboard'
import { Network, Wallets, DappId } from '@/config.js'
import { mapState, mapMutations } from 'vuex'
export default {
	data() {
		return {
			metaMaskAddress: '',
			networkId: null
		}
	},
	watch: {
		metaMaskAddress(cur, old) {
			this.setMetaMaskAddress(cur)
		},
		networkId(cur, old) {
			// this.editNet()
			this.setNetworkId(cur)
		}
	},
	methods: {
		...mapMutations(['setMetaMaskAddress', 'setNetworkId', 'setPendings']),
		async editNet() {
			await Vue.prototype.$onboard.walletCheck()
			await Vue.prototype.$onboard.getState()
		},
		async login() {
			try {
				await Vue.prototype.$onboard.walletSelect()
				await Vue.prototype.$onboard.walletCheck()
				await Vue.prototype.$onboard.accountSelect()
			} catch (error) {
				console.log(error)
			}
		},
		async onConnect() {
			const wallets = Wallets
			const dappId = DappId // [String] The API key created by step one above
			const networkId = Network // [Integer] The Ethereum network ID your Dapp uses.
			Vue.prototype.$onboard = Onboard({
				dappId,
				hideBranding: false,
				networkId,
				//... other options
				subscriptions: {
					wallet: (wallet) => {
						Vue.prototype.$web3 = !wallet.provider
							? null
							: new Web3(wallet.provider)
						const walletName = !wallet.name ? 'NoWallet' : wallet.name
						window.sessionStorage.setItem('EarningSelectedWallet', walletName)
					},
					address: (address) => {
						this.metaMaskAddress =
							typeof address === 'undefined' ? '' : address.toLowerCase()
					},
					network: (network) => {
						this.networkId =
							typeof network === 'undefined' ? null : network + ''
					},
					balance: (balance) => {
						console.log(balance, 'balance')
					}
				},
				walletSelect: {
					wallets: wallets
				}
			})

			let previouslySelectedWallet = null
			const onboard = Vue.prototype.$onboard
			if (onboard) {
				previouslySelectedWallet = window.sessionStorage.getItem(
					'EarningSelectedWallet'
				)
				if (
					previouslySelectedWallet &&
					previouslySelectedWallet !== 'NoWallet'
				) {
					await Vue.prototype.$onboard.walletSelect(previouslySelectedWallet)
					await Vue.prototype.$onboard.walletCheck()
				}
			}
		},
		async resetApp() {
			Vue.prototype.$onboard.walletReset()
		}
	}
}
</script>
