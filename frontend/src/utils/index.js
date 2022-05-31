// import { BigNumber } from 'bignumber.js'

const copys = (thit, metaMaskAddress) => {
	const spanText = metaMaskAddress
	const oInput = document.createElement('input')
	oInput.value = spanText
	document.body.appendChild(oInput)
	oInput.select() // 选择对象
	document.execCommand('Copy') // 执行浏览器复制命令
	oInput.className = 'oInput'
	oInput.style.display = 'none'
	document.body.removeChild(oInput)
	thit.$message({
		message: 'Copy success!',
		type: 'success',
		offset: 100
	})
}

const ellipsis = (value, one = 0, two = 6, three = 38, four = 42) => {
	if (!value) return ''
	if (value.length > 10) {
		return value.slice(one, two) + '...' + value.slice(three, four)
	}
	return value
}

const dividedBy = (balance, num) => {
	if (!Number(balance)) return 0
	return new BigNumber(balance).dividedBy(num).toString(10)
}
const setConfirmValue = (balance, num) => {
	if (!Number(balance)) return 0
	return new BigNumber(balance).multipliedBy(num).toFixed(0, 1)
}
const multipliedByFixed = (balance, fee, del) => {
	if (!Number(balance)) return 0
	return new BigNumber(balance).multipliedBy(fee).toFixed(del, 1)
}
const setAssetsValue = (balance, num) => {
	if (!Number(balance)) return 0
	return new BigNumber(num).multipliedBy(balance).dividedBy(100).toString(10)
}
const setWithdrawValue = (balance, lp_token, user_assets) => {
	if (!Number(balance)) return 0
	if (!Number(user_assets)) return 0
	return new BigNumber(balance)
		.dividedBy(user_assets)
		.multipliedBy(lp_token)
		.toFixed(0, 1)
}
//小于等于
const isLessThanOrEqualTo = (num1, num2) => {
	return new BigNumber(num1).lte(num2)
}
//小于lt
const isLt = (num1, num2) => {
	return new BigNumber(num1).lt(num2)
}
//小于钱包余额-0.1
const minusLet=(num1, num2) => {
	return new BigNumber(num1).lte( new BigNumber(num2).minus(0.1))
}
//ETH-0.1
const minus=( num2) => {
  if(new BigNumber(num2).minus(0.1).lt(0)){
    return 0
  }else{
    return  new BigNumber(num2).minus(0.1)
  }
}
//生成随机数
const random = (lower, upper) => {
	return Math.floor(Math.random() * (upper - lower)) + lower
}
export {
	dividedBy,
	setConfirmValue,
	copys,
	ellipsis,
	setAssetsValue,
	setWithdrawValue,
	isLessThanOrEqualTo,
	random,
	multipliedByFixed,
  isLt,
  minusLet,
  minus
}
