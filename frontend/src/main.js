// import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './utils/prototype.js'
import './icons'
// import ElementUI from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css'
import SendTransactionMixin from './components/SendTransactionMixin'
import { ntf } from './components/notify'

Vue.mixin(ntf)
// Vue.use(ElementUI)
Vue.mixin(SendTransactionMixin)

new Vue({
	router,
	store,
	render: (h) => h(App)
}).$mount('#app')
