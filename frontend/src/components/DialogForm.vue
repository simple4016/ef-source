<template>
	<div class="dialogbody">
		<el-dialog
			:visible.sync="dialogVisible"
			:width="diaWidth"
			:before-close="handleClose"
			:fullscreen="fullscreen"
			:title="title"
			:show-close="close"
			height="100px"
			center
		>
			<slot />
		</el-dialog>
	</div>
</template>

<script>
export default {
	props: {
		dialogVisible: {
			type: Boolean,
			default: false
		},
		diaWidth: {
			type: String,
			default: '40%'
		},
		fullscreen: {
			type: Boolean,
			default: false
		},
		title: {
			type: String,
			default: ''
		},
		close: {
			type: Boolean,
			default: true
		}
	},
	data() {
		return {}
	},
	methods: {
		handleClose(done) {
			this.$emit('closeMain', false)
			this.$emit('closeShow', false)
		}
	}
}
</script>
<style lang="scss" scoped>
.dialogbody {
	height: 100%;
	width: 100%;
}
/deep/ .el-dialog {
	border-radius: 20px !important;
	// background-color:
}
.submit_button {
	width: 120px;
	border-radius: 20px;
}
.dialog-box {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
	img {
		width: 20%;
		padding: 30px;
	}
	li {
		list-style-type: none;
		font-size: 16px;
		color: rgba(86, 101, 112, 1);
	}
}
</style>
