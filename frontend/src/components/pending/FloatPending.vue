<template>
	<transition>
		<div
			ref="dragIcon"
			class="dragIcon"
			v-show="Pendings.length > 0"
			:style="{
				left: IsPhone ? left + 20 + 'px' : left + 'px',
				top: top + 'px',
				width: itemWidth + 'px',
				height: itemHeight + 'px'
			}"
		>
			<i class="el-icon-loading"></i>
			{{ Pendings.length }}
			{{ text }}
		</div>
	</transition>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
import NotifyMixin from './NotifyMixin'
import { getTransactionReceipt, getTransaction } from '@/common/web3'
export default {
	mixins: [NotifyMixin],
	props: {
		text: {
			type: String,
			default: '球'
		},
		itemWidth: {
			type: Number,
			default: 150
		},
		itemHeight: {
			type: Number,
			default: 40
		}
	},
	computed: {
		...mapState(['MetaMaskAddress', 'Pendings', 'NetworkId', 'IsPhone'])
	},
	data() {
		return {
			left: 0,
			top: 90,
			Pending: [],
			types: [],
			timerTransaction: null,
			currentTop: null,
			currentleft: null,
			clientW: document.body.clientWidth, // 视口宽
			clientH: document.body.clientHeight // 视口高
		}
	},
	watch: {
		MetaMaskAddress(cur, old) {
			if (cur) {
				this.getPendingList()
				this.startTransactionTimer()
			}
		},
		Pendings(cur, old) {
			console.log(cur, 'curcurcurcurcurcurcurcurcurcur')
		},
		clientW(cur, old) {
			this.left = cur - this.itemWidth - 40
		}
	},
	created() {
		this.left = this.clientW - this.itemWidth - 40
	},
	mounted() {
		this.getPendingList()
		this.startTransactionTimer()
		window.onresize = () => {
			return (() => {
				this.clientW = document.body.clientWidth
				this.left = this.clientW - this.itemWidth - 40
			})()
		}
	},
	methods: {
		...mapMutations(['setPendings']),
		getPendingList() {
			if (!this.MetaMaskAddress) return
			const Pending = localStorage.getItem('EarningFarmPending')
				? JSON.parse(localStorage.getItem('EarningFarmPending'))
				: []
			const Pendings =
				Pending.length > 0
					? Pending.filter((item) => item.id === this.MetaMaskAddress)
					: []
			localStorage.setItem('EarningFarmPending', JSON.stringify(Pendings))
			this.setPendings(Pendings)
		},
		startTransactionTimer() {
			clearInterval(this.timerTransaction)
			this.timerTransaction = null
			this.timerTransaction = setInterval(() => {
				this.getTransactionStatus()
			}, 6000)
		},
		async getTransactionStatus() {
			if (!this.MetaMaskAddress) return
			if (this.Pendings.length === 0) return
			const data = await getTransaction(this.Pendings[0].hash)
			console.log(data, 'data--------')
			try {
				if (data) {
					if (data.blockHash) {
						const status = await getTransactionReceipt(this.Pendings[0].hash)
						console.log(status, 'statusstatusstatusstatus')
						if (status && status.transactionHash === this.Pendings[0].hash) {
							const type = status.status ? 'success' : 'error'
							const name = status.status
								? `Transaction Success`
								: `Transaction Fail`
							const arr = [...this.Pendings]
							arr.splice(0, 1)
							localStorage.setItem('EarningFarmPending', JSON.stringify(arr))
							this.setPendings(arr)
							this.openMessageTips(name, status.transactionHash, type)
						} else {
							const arr = [...this.Pendings]
							arr.splice(0, 1)
							localStorage.setItem('EarningFarmPending', JSON.stringify(arr))
							this.setPendings(arr)
						}
					}
				} else {
					const arr = [...this.Pendings]
					arr.splice(0, 1)
					localStorage.setItem('EarningFarmPending', JSON.stringify(arr))
					this.setPendings(arr)
				}
			} catch (error) {
				const arr = [...this.Pendings]
				arr.splice(0, 1)
				localStorage.setItem('EarningFarmPending', JSON.stringify(arr))
				this.setPendings(arr)
			}
		}
	},
	destroyed() {
		clearInterval(this.timerTransaction)
		this.timerTransaction = null
	}
}
</script>

<style scoped lang="scss">
.dragIcon {
	position: fixed;
	// @include hd_color($hd-background-color-theme);
	background-color: #409eff;
	box-shadow: 0px 0px 6px #66b1ff;
	border-radius: 20px;
	color: #fff;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 14px;
	cursor: pointer;
	z-index: 999;
	i {
		margin-right: 10px;
	}
}

.v-enter {
	opacity: 1;
}

.v-leave-to {
	opacity: 0;
}

.v-enter-active,
.v-leave-active {
	transition: opacity 0.3s;
}
</style>
