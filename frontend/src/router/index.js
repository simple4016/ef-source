// import Vue from 'vue'
// import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const routes = [
	{ path: '/', redirect: '/index' },
	{
		path: '/index',
		name: 'index',
		component: () => import('../views/Index.vue'),
		meta: {
			title: '主页'
			// requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
		}
	},
	{
		path: '/home',
		name: 'Home',
		component: Home,
		children: [
			{
				path: '/',
				redirect: '/invest'
			},
			{
				path: '/invest',
				name: 'invest',
				component: () => import('../views/cff/Cff.vue')
			}
		]
	}
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
})
export default router
