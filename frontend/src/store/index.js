// import Vue from 'vue'
// import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		MetaMaskAddress: '',
		NetworkId: 0,
		Pendings: [],
		IsPhone: false
	},
	mutations: {
		setNetworkId(state, val) {
			state.NetworkId = val
		},
		setMetaMaskAddress(state, val) {
			state.MetaMaskAddress = val
		},
		setPendings(state, val) {
			state.Pendings = val
		},
		setIsPhone(state, val) {
			state.IsPhone = val
		}
	},
	actions: {},
	modules: {}
})
