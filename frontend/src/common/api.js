import qs from 'qs'
import fetch from '../utils/Fetch'
import { API_URL, Network } from '../config.js'
const NET = Network === 1 ? 'm' : ''
const URL = API_URL + '/' + NET
// const API_URL = 'http://10.10.10.207:8581'
const getAsset = (data, code = '') => {
	return fetch({
		url: `${URL + code}/getAsset`,
		method: 'POST',
		data: qs.stringify({ address: data })
	})
}
const getProfit = (code = '') => {
	return fetch({
		url: `${URL + code}/profit`,
		method: 'POST'
	})
}
const getTransaction = (data, code = '') => {
	return fetch({
		url: `${URL + code}/transaction`,
		method: 'POST',
		data: qs.stringify(data)
	})
}
//首页
const getSevendayProfit = (code) => {
	return fetch({
		url: `${URL + code}/getAsset`,
		method: 'POST',
		data: qs.stringify({ firstpage: true })
	})
}
export { getAsset, getProfit, getTransaction, getSevendayProfit }
