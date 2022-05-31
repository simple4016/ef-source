<template>
	<div class="home">
		<el-container direction="vertical" class="body">
			<el-header> <header-bar /> </el-header>
			<el-main>
				<router-view />
			</el-main>
			<el-footer> <footer-bar /></el-footer>
			<float-pending :text="'Pending'" :itemWidth="itemWidth"></float-pending>
		</el-container>
	</div>
</template>

<script>
import { mapState } from 'vuex'
import HeaderBar from '@/components/HeaderBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import FloatPending from '../components/pending/FloatPending.vue'
export default {
	name: 'Home',
	components: {
		HeaderBar,
		FooterBar,
		FloatPending
	},
	computed: {
		...mapState(['IsPhone']),
		itemWidth() {
			return this.IsPhone ? 130 : 150
		}
	}
}
</script>
<style scoped lang="scss">
.el-header {
	height: 80px !important;
	padding: 0 !important;
	box-sizing: none !important;
	font-size: 28px;
	color: rgba(86, 101, 112, 1);
	background: rgba(255, 255, 255, 1);
	display: flex;
	justify-content: center;
}
.home {
	height: 100%;
	width: 100%;
}
.el-container.is-vertical {
	height: 100%;
}
.el-main {
	padding: 0 !important;
	box-sizing: none !important;
	display: flex;
	// align-items: center;
	justify-content: center;
	overflow: initial;
	background: #f5f5f5;
	width: 100%;
	margin: 0 auto;
}

.el-footer {
	height: 80px !important;
	background: rgba(86, 101, 112, 1);
}

.el-container {
	height: 100%;
	width: 100%;
}
@media screen and (max-width: 768px) {
	.el-header {
		margin: 0 !important;
		padding: 0 !important;
	}
	.el-footer {
		height: auto !important;
	}
}
</style>
