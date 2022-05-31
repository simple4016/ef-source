<template>
	<div class="high-home">
		<ul
			v-for="(item, idx) in list"
			:key="idx"
			:class="{ 'ul-border': item.showContent }"
		>
			<div class="svg-icon">High Risk</div>
			<div
				class="title"
				:style="{ padding: item.code === 'ETH' ? '25px 30px' : '13px 30px' }"
			>
				<el-row>
					<el-col :span="6">
						<div class="title_text">
							<img
								class="title_img"
								:src="require('../../assets/imgs/' + item.code + '.png')"
								alt
							/>
							<span>{{
								item.code === 'WBTC' ? 'BTC/' + item.code : item.code
							}}</span>
							<span v-show="item.code === 'ETH'" class="leve">Leveraged</span>
						</div>
					</el-col>
					<el-col :span="4">
						<div>
							<li class="top_l3">
								<el-tooltip class="item" effect="dark" placement="top">
									<div slot="content">
										Asset: Personal total assets in USDC calculated in real time
										based on Curve pools.
										<br />Due to slipage when withdraw, number withdrew would
										have slight difference than Asset number.
										<br />
										Accu Yield: Calculated based on numbers when doing yield
										farming.
									</div>
									<span> Personal</span>
								</el-tooltip>
							</li>
							<li class="top_li">Asset</li>
							<li class="bom_li">
								{{ $nameFixed(item.user_assets, item.code) }}
								<br />
								<span class="myorigin" v-if="item.code !== 'ETH'">
									≈
									{{ $nameFixed(item.user_assets_origin, item.code) }} CRV</span
								>
								<div v-else class="top_l2" v-show="item.code !== 'ETH'"></div>
							</li>
						</div>
					</el-col>
					<el-col :span="4">
						<div>
							<li class="top_l2"></li>
							<li class="top_li">
								Accu Yield
								<el-tooltip
									class="item"
									effect="dark"
									placement="top"
									v-if="item.code !== 'ETH'"
								>
									<div slot="content">
										1. Deposited USDC will be converted into CRV, so Accu Yield
										will be negative in a short term.
										<br />
										2. CRV price fluctuates, so Accu Yield also fluctuates
										because the backend asset of this strategy is CRV.
										<br />
										We recommend you wait for a better time to withdraw when the
										Accu Yield if negative.
									</div>
									<i class="el-icon-question"></i>
								</el-tooltip>
							</li>
							<li class="bom_li">
								{{ $nameFixed(item.user_profit, item.code) }}
								<div class="top_l2" v-show="item.code !== 'ETH'"></div>
							</li>
						</div>
					</el-col>

					<el-col :span="2">
						<div>
							<el-divider direction="vertical"></el-divider>
						</div>
					</el-col>
					<el-col :span="4">
						<div>
							<li class="top_l3">
								<el-tooltip class="item" effect="dark" placement="top">
									<div slot="content">
										7 Days APY: Calculated by the past 7 days daily APR in
										average.
									</div>
									<span>Protocol</span>
								</el-tooltip>
							</li>

							<li class="top_li">Asset</li>
							<li class="bom_li">
								{{ $nameFixed(item.totalassets, item.code) }}
							</li>
							<div class="top_l2" v-show="item.code !== 'ETH'"></div>
						</div>
					</el-col>
					<el-col :span="4">
						<div>
							<li class="top_l2"></li>
							<li class="top_li">7 Days APY</li>
							<li class="bom_li">
								{{ $numFixed(item.sevendayProfit, 1) + '%' }}
							</li>
							<div class="top_l2" v-show="item.code !== 'ETH'"></div>
						</div>
					</el-col>
					<el-col :span="1">
						<i
							:class="
								item.showContent ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
							"
							style="cursor: pointer"
							@click="changeContent(item)"
						></i>
					</el-col>
				</el-row>
			</div>

			<div v-if="item.showContent" class="bottom">
				<div class="body">
					<el-row>
						<el-col :span="4">
							<span class="bom_li">Strategy</span>
						</el-col>
						<el-col :span="9">
							<span class="spanText">{{ textList[item.code] }}</span>
							<br />
							<span class="spanText"
								>{{ $feeRatio(item.feeRatio) }}%
								{{
									item.code === 'ETH'
										? 'of interest gained will be charged as processing fee.'
										: 'of yielding rewards will be charged as processing fee.'
								}}
							</span>
						</el-col>
						<el-col :span="5">
							<div>
								<el-button
									style="float: right"
									type="warning"
									@click="selectLine"
									plain
								>
									View Trend
								</el-button>
							</div>
						</el-col>
						<el-col :span="5">
							<div>
								<el-button
									style="float: right"
									type="warning"
									@click="selectTable"
									plain
								>
									View History
								</el-button>
							</div>
						</el-col>
					</el-row>
				</div>
				<div class="body_text">
					<div>
						<el-row>
							<el-col :span="10">
								<li class="bom_li" style="margin-bottom: 10px">
									<span class="input_span">
										Wallet Balance:
										{{ $nameFixed(totalOf, item.code) }}
										<span>{{
											item.code === 'ETH' ? item.code : selectConfirm
										}}</span>
									</span>
								</li>
								<li class="input_li">
									<el-input
										v-model="confirmInput"
										@input="inputConfirm"
										@focus="Max = 1"
										onkeyup="value=value.replace(/[^\d^\.]/g,'')"
										:style="{ 'border-color': Max === 1 ? '#fd8465' : '' }"
									>
										<template slot="append">
											<span
												:style="{
													'margin-right': item.code === 'ETH' ? '0px' : '20px'
												}"
												class="Max"
												v-show="Max === 1"
												@click="setMax(Max, totalOf)"
												>{{ item.code === 'ETH' ? 'SAFE MAX' : 'MAX' }}</span
											>
										</template>
										<template slot="append" v-if="item.code !== 'ETH'">
											<el-select
												v-model="selectConfirm"
												:popper-append-to-body="false"
												slot="prepend"
												@change="selectConfirmChange"
											>
												<el-option label="USDC" value="USDC"></el-option>
												<el-option label="CRV" value="CRV"></el-option>
											</el-select>
										</template>
									</el-input>
								</li>
								<li>
									<el-slider
										v-model="confirmVal"
										:step="25"
										:marks="marks"
										@change="setConfirmVal"
										show-stops
										:show-tooltip="false"
									></el-slider>
								</li>
							</el-col>
							<el-col :span="10" :offset="3">
								<div>
									<li class="bom_li" style="margin-bottom: 10px">
										<span class="input_span">
											Asset Deposited: ≈
											{{
												$nameFixed(
													selectWithdraw === 'USDC' || selectWithdraw === 'ETH'
														? item.user_assets
														: item.user_assets_origin,
													item.code
												)
											}}
											<span>{{
												item.code === 'ETH' ? item.code : selectWithdraw
											}}</span>
											<el-tooltip
												class="item"
												effect="dark"
												placement="top-end"
												v-if="item.code !== 'ETH'"
											>
												<div slot="content">
													Calculated based on Curve virtual price. May have
													slight difference when withdrawing.
												</div>
												<i class="el-icon-question"></i>
											</el-tooltip>
										</span>
									</li>
									<li class="input_li">
										<el-input
											v-model="withdrawInput"
											@input="inputWithdraw"
											@focus="Max = 2"
											onkeyup="value=value.replace(/[^\d^\.]/g,'')"
											:style="{ 'border-color': Max === 2 ? '#fd8465' : '' }"
										>
											<template slot="append">
												<span
													:style="{
														'margin-right': item.code === 'ETH' ? '0px' : '20px'
													}"
													class="Max"
													v-show="Max === 2"
													@click="setMax(Max, item)"
													>MAX</span
												>
											</template>
											<template slot="append" v-if="item.code !== 'ETH'">
												<el-select
													v-model="selectWithdraw"
													@change="selectWithdrawChange"
													slot="prepend"
													:popper-append-to-body="false"
												>
													<el-option label="USDC" value="USDC"></el-option>
													<el-option label="CRV" value="CRV"></el-option>
												</el-select>
											</template>
										</el-input>
									</li>
									<li>
										<el-slider
											v-model="withdrawVal"
											:step="25"
											:marks="marks"
											@change="setWithdrawVal"
											show-stops
											:show-tooltip="false"
										></el-slider>
									</li>
								</div>
							</el-col>
						</el-row>
						<el-row>
							<el-col :span="10">
								<el-button
									type="warning"
									plain
									style="float: right; width: 45%"
									v-if="item.code !== 'ETH' && isApprove"
									@click="approve"
									>Approve
								</el-button>
								<el-button
									type="warning"
									plain
									style="float: right; width: 45%"
									v-else
									@click="confirm(item)"
								>
									Deposit</el-button
								>
							</el-col>
							<el-col :span="10" :offset="3">
								<el-button
									type="warning"
									plain
									style="float: right; width: 50%"
									@click="withdrawItem(item)"
								>
									Withdraw</el-button
								>
							</el-col>
						</el-row>
					</div>
				</div>
			</div>
		</ul>

		<dialog-form
			:dialogVisible="dialogVisible"
			:diaWidth="diaWidth"
			:title="title"
			@closeMain="closeMain"
			v-if="dialogVisible"
		>
			<component
				:is="currentName"
				:echartsData="echartsData"
				:codeurl="codeurl"
				codeType="true"
				:eHeight="'400px'"
				:code="itemData.code"
			/>
		</dialog-form>

		<dialog-form
			:dialogVisible="isYield"
			diaWidth="70%"
			@closeMain="closeisYield"
			v-if="isYield"
		>
			<div>
				CRV price fluctuates, so Accu Yield also fluctuates because the backend
				asset of this strategy is CRV. We recommend you wait for a better time
				to withdraw when the Accu Yield if negative.
			</div>
			<button class="yieldbtn" @click="withdraw(itemData)">Confirm</button>
		</dialog-form>
	</div>
</template>

<script>
import EchartsLine from './EchartsLine.vue'
import CffTable from './CffTable.vue'
import DialogForm from '../../components/DialogForm.vue'
import HighRiskMixin from '../../components/mixins/HighRiskMixin'
export default {
	name: 'HighRisk',
	mixins: [HighRiskMixin],
	components: {
		DialogForm,
		EchartsLine,
		CffTable
	},
	computed: {
		currentName() {
			switch (this.dialogName) {
				case 'EchartsLine':
					return EchartsLine
				case 'CffTable':
					return CffTable
				default:
					return ''
			}
		}
	}
}
</script>
<style scoped lang="scss">
/deep/ .el-select-dropdown__item {
	padding: 0 !important;
	padding-left: 20px !important;
}
/deep/ .el-select-dropdown__item.selected {
	padding: 0;
	padding-left: 20px;
	color: #fd8465;
}
.leve {
	border: 1px solid #2196f3;
	color: #2196f3 !important;
	font-size: 13px !important;
	background: #ecf5ff;
	padding: 5px 14px;
	margin: 0 10px;
	border-radius: 4px;
}
.yieldbtn {
	color: #fff;
	background-color: #409eff;
	border-color: #409eff;
	width: 120px;
	height: 30px;
	border: none;
	border-radius: 30px;
	margin: 0 auto;
	display: block;
	margin-top: 26px;
	cursor: pointer;
}
.el-icon-question:hover {
	color: #fd8465;
}
.high-home {
	ul {
		border-radius: 36px;
		border: 1px solid #aab1b7;
		padding-inline-start: 0;
		background-color: #fff;
		margin-bottom: 10px;
		min-height: 170px;
		position: relative;
		.svg-icon {
			font-size: 13px;
			background-color: #ffefeb;
			color: #fd8465;
			border-radius: 4px;
			padding: 5px 14px;
			position: absolute;
			right: 60px;
		}
		li {
			list-style-type: none;
			padding: 5px 0;
		}
	}
	ul:hover {
		border-color: #fd8465;
		box-shadow: 0px 0px 8px rgba(226, 106, 75, 0.23);
	}
	ul:focus {
		border-color: #fd8465;
		box-shadow: 0px 0px 8px rgba(226, 106, 75, 0.23);
	}
	.ul-border {
		border-color: #fd8465;
		box-shadow: 0px 0px 8px rgba(226, 106, 75, 0.23);
	}
	.title {
		.el-row {
			padding: 10px 0;
			display: flex;
			align-items: center;
			width: 100%;
			.el-divider--vertical {
				height: 52px;
			}
			// .el-col {
			//   padding: 0 10px;
			// }
			li {
				white-space: normal;
				word-break: break-all;
				word-wrap: break-word;
			}
		}
	}

	.title_img {
		width: 20%;
	}

	.title_text {
		display: flex;
		align-items: center;

		span {
			padding-left: 5px;
			font-size: 18px;
			color: #566570;
			font-weight: 500;
		}
	}

	.top_li {
		font-size: 14px;
		color: rgba(147, 156, 163, 1);
	}

	.top_l3 {
		font-size: 14px;
		height: 25px;
		color: #566570;

		span {
			cursor: help;
		}
	}

	.top_l2 {
		font-size: 14px;
		height: 25px;
		color: #fff;
	}

	.bom_li {
		font-size: 18px;
		// height: 10px;
		color: #566570;
		.myorigin {
			font-size: 12px;
			color: #939ca3;
		}
		.showWbtc {
			float: right;
			font-size: 14px;
			color: #409eff;
			border-bottom: 1px solid #409eff;
			cursor: pointer;
		}
	}

	.bottom {
		padding-left: 30px;
		background: #fff6f4;
		border-radius: 0 0 36px 36px;
	}

	.body {
		padding: 30px 0;

		.el-button {
			border-radius: 30px;
		}

		.spanText {
			font-size: 14px;
			color: #939ca3;
		}
	}

	.el-button {
		width: 90%;
		font-size: 14px;
	}

	.body_text {
		.el-row {
			padding: 10px 0;
			display: flex;
			align-items: center;
		}

		.el-button {
			border-radius: 30px;
		}
	}

	.input_span {
		float: right;
		font-size: 14px;
		color: #566570;
		// cursor: pointer;
		margin-bottom: 5px;
	}

	.Max {
		background-color: #ffa267;
		border-radius: 50px;
		padding: 0 10px;
		color: #fff;
		margin-right: 20px;
		cursor: pointer;
	}
	/deep/ .el-select {
		width: 90px !important;
	}
	/deep/ .el-input-group__append {
		background-color: transparent !important;
		border: none !important;
		border-radius: 36px;
	}

	/deep/ .el-input__inner {
		border: none !important;
		background-color: transparent !important;
		border-radius: 36px;
	}

	/deep/ .el-slider__button-wrapper {
		z-index: 0 !important;
	}

	.input_li {
		// border: 1px solid rgba(204, 208, 211, 1);
		// border-radius: 36px;
		padding: 0;
		margin: 5px 0;
	}

	.el-input {
		border: 1px solid rgba(204, 208, 211, 1);
		border-radius: 36px;
	}

	.el-input:hover {
		border: 1px solid #fd8465;
		border-radius: 36px;
	}

	.el-input:active {
		border: 1px solid #fd8465;
		border-radius: 36px;
	}

	.el-input:focus {
		border: 1px solid #fd8465;
		border-radius: 36px;
	}
	/deep/ .el-slider__button {
		width: 10px;
		height: 10px;
		border-color: #fd8465;
	}
	/deep/ .el-slider__bar {
		background-color: #fd8465;
	}
	.el-col-10 {
		position: relative;
	}
	.ratio {
		position: absolute;
		bottom: 0px;
		// margin-left: 25%;
		font-size: 14px;
		color: #ffa267;
	}
}
/deep/ .el-button--warning.is-plain {
	border-color: #fd8465;
	color: #fd8465;
	background-color: #fff1ee;
}
/deep/ .el-button--warning.is-plain:hover {
	border-color: #fd8465;
	color: #fff;
	background-color: #fd8465;
}
</style>
