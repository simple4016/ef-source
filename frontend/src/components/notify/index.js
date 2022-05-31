const ntf = {
	methods: {
		Success(msg, title = 'Success', offset = 120, duration = 0) {
			this.$notify({
				type: 'success',
				title: title,
				message: msg,
				offset: offset,
				duration: duration
			})
		},
		Warning(msg, title = 'Warning', offset = 120, duration = 5000) {
			this.$notify({
				type: 'warning',
				title: title,
				message: msg,
				offset: offset,
				duration: duration
			})
		},
		Error(msg, title = 'Error', offset = 120, duration = 0) {
			this.$notify({
				type: 'error',
				title: title,
				message: msg,
				offset: offset,
				duration: duration
			})
		}
	}
}
export { ntf }
