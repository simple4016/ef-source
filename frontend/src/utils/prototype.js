import Web3 from 'web3'
// import Vue from 'vue'
Vue.prototype.$web3 = new Web3(Web3.givenProvider)

Vue.prototype.$nameFixed = (num, name) => {
	if (!Number(num)) return 0
	const wei = name === 'USDC' ? 2 : name === 'ETH' ? 4 : 8
	return new BigNumber(num).toFixed(wei, 1)
}

Vue.prototype.$numFixed = (val, key = 0) => {
	return key !== 0
		? new BigNumber(val).multipliedBy(100).toFixed(2, 1)
		: new BigNumber(val).toFixed(2, 1)
}

Vue.prototype.$feeRatio = (val) => {
	if (!Number(val)) return 0
	return new BigNumber(val).multipliedBy(100).toFixed(0, 1)
}
