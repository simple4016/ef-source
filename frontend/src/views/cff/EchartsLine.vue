<template>
	<div ref="chart" style="width: 100%" :style="{ height: eHeight }" />
</template>
<script>
import dayjs from 'dayjs'
import { BigNumber } from 'bignumber.js'
const echarts = require('echarts')
export default {
	name: 'EchartsLine',
	props: {
		eHeight: {
			type: String,
			default: '400px'
		},
		echartsData: {
			type: Array,
			default: () => {
				return []
			}
		}
	},
	mounted() {
		let utc = require('dayjs/plugin/utc')
		dayjs.extend(utc)
		let dom = this.$refs.chart
		let myChart = echarts.init(dom)
		let option = {
			backgroundColor: 'rgba(255, 255, 255, 1)',
			//鼠标移入刻度线
			tooltip: {
				trigger: 'axis',
				// axisPointer: {
				//   type: 'cross',
				//   label: {
				//     backgroundColor: '#6a7985',
				//     fontSize: 12,
				//   },
				// },
				// textStyle: { fontSize: '100%' },
				formatter: (v) => {
					return `
              <div class='u-p-2'>
                <div class='fz-10'>${'Date：' + v[0].axisValue}</div>
                <div class='fz-10 u-mt-2'>${
									'APR：' + Number(v[0].value).toFixed(2) + '%'
								}</div>
              </div>
            `
				}
			},
			//位置
			grid: {
				top: '5%',
				left: '12%',
				right: '3%',
				bottom: '8%'
				// containLabel: true
			},
			xAxis: [
				{
					type: 'category',
					color: '#59588D',
					axisLabel: {
						color: '#282828'
					},
					splitLine: {
						// show: true
					},

					axisLine: {
						show: true,
						lineStyle: {
							color: 'rgba(185, 210, 225, 1)'
						}
					},
					axisTick: {
						show: false
					},
					// boundaryGap: true,
					data:
						this.echartsData && this.echartsData.length > 0
							? this.echartsData.map((item) =>
									dayjs.utc(Number(item.date) * 1000).format('YYYY-MM-DD')
							  )
							: []
				}
			],

			yAxis: [
				{
					type: 'value',
					splitNumber: 4,
					axisLabel: {
						show: true,
						// margin: 20,
						textStyle: {
							color: '#737373'
						},
						formatter: (value) => {
							return value + '%'
						}
					},
					axisTick: {
						show: false
					},
					splitLine: {
						lineStyle: {
							type: 'dashed',
							color: 'rgba(185, 210, 225, 1)'
						}
					},
					axisLine: {
						show: true,
						lineStyle: {
							color: 'rgba(185, 210, 225, 1)'
						}
					}
				}
			],
			series: [
				{
					name: '',
					type: 'line',
					smooth: true, //是否平滑
					showSymbol: false,
					showAllSymbol: true,
					symbol: 'circle',
					symbolSize: 10,
					lineStyle: {
						normal: {
							color: 'rgba(255, 162, 103, 1)'
						}
					},
					label: {
						show: false,
						position: 'top',
						textStyle: {
							color: 'rgba(255, 162, 103, 1)'
						}
					},

					itemStyle: {
						color: 'rgba(255, 162, 103, 1)',
						borderColor: 'rgba(255, 162, 103, 1)'
					},
					tooltip: {
						show: true
					},
					areaStyle: {
						normal: {
							color: new echarts.graphic.LinearGradient(
								0,
								0,
								0,
								1,
								[
									{
										offset: 0,
										color: 'rgba(255, 162, 103, 1)'
									},
									{
										offset: 1,
										color: 'rgba(255, 162, 103, 0.1)'
									}
								],
								false
							),
							shadowColor: 'rgba(255, 162, 103, 1)',
							shadowBlur: 20
						}
					},
					data:
						this.echartsData && this.echartsData.length > 0
							? this.echartsData.map((item) => {
									return new BigNumber(item.profit)
										.multipliedBy(100)
										.toString(10)
							  })
							: []
				}
			]
		}
		myChart.setOption(option)
	}
}
</script>
