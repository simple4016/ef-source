<template>
	<div id="app">
		<router-view />
	</div>
</template>

<script>
import { mapMutations } from 'vuex'
import WalletMixin from './components/dialog-wallet/WalletMixin'
export default {
	name: 'App',
	mixins: [WalletMixin],
	mounted() {
		this.onConnect()
		this.clientW = document.body.clientWidth
		const isPhone = this.clientW < 768 ? true : false
		this.setIsPhone(isPhone)
	},
	methods: {
		...mapMutations(['setIsPhone'])
	}
}
</script>

<style lang="scss">
html,
body,
#app {
	height: 100%;
	width: 100%;
	margin: 0;
	padding: 0;
	font-family: 'PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'Microsoft YaHei',
		'WenQuanYi Micro Hei', sans-serif;
}
</style>
