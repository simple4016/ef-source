<script>
import { OPEN_URL } from '../../config.js'
export default {
	methods: {
		openHash(hash) {
			const Hash = hash.substr(0, 2) === '0x' ? hash : '0x' + hash
			const Win = window.open()
			Win.opener = null
			Win.location = OPEN_URL + Hash
		},
		// type ? success :error
		openMessageTips(title, hash, type, offset = 120, duration = 0) {
			const _this = this
			const h = this.$createElement
			this.$notify({
				position: 'top-right',
				dangerouslyUseHTMLString: true,
				title: title,
				type: type,
				offset: offset,
				duration: duration,
				customClass: type + 'color',
				message: h('div', { class: 'message' }, [
					h(
						'span',
						{
							style: 'cursor: pointer;',
							on: {
								click: this.openHash.bind(_this, hash)
							}
						},
						'View on Etherscan'
					)
				])
			})
		}
	}
}
</script>
<style lang="scss" scoped>
.message {
	width: 50%;
	background-color: #cffdd9;
}
</style>
