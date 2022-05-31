// import axios from 'axios'
const service = axios.create({
	withCredentials: true, // 跨域请求时发送Cookie
	// headers: {
	// 	'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	// },
	timeout: 60000
})
service.interceptors.request.use(
	(config) => {
		const token = sessionStorage.getItem('token')
		if (token) {
			config.headers['auth-token'] = token
		}
		return config
	},
	(error) => {
		Promise.reject(error)
	}
)

service.interceptors.response.use(
	(response) => {
		if (response.data.resultCode === 100) {
			return response.data
		} else {
			return false
		}
	},
	(error) => {
		console.log(error)
		return false
	}
)
export default service
