<template>
	<view class="flex flex-column" v-watermark="watermarkConfig">
		<block v-if="pricelist.length > 0 && isread">
			<view class=" flex-1">
				<view class="flex start" style="padding: 5px 10px;align-items: center;">
					起运港：<uni-icons type="location" style="font-size: x-large;"></uni-icons>
					<text style="font-size:18px;font-weight: 700;">{{pricelist[0].pol}}</text>
				</view>
				<view style="border-bottom: 1px solid rgb(234 234 234);margin-bottom: 1rpx;" />
				<view class="flex start" style="padding: 5px 10px;display: flex;align-items: center;">
					目的港：<uni-icons type="location-filled" style="font-size: x-large;"></uni-icons>
					<text style="font-size:18px;font-weight: 700;">{{pricelist[0].pod}}</text>
				</view>
			</view>
			<view style="border-bottom: 1px solid #e5e5e5;margin-bottom: 10rpx;" />
			<uni-table ref="table" stripe emptyText="暂无更多数据">
				<uni-tr>
					<uni-th width="55" align="center">船公司</uni-th>
					<uni-th width="50" align="center">20GP<br>(USD)</uni-th>
					<uni-th width="50" align="center">40GP<br>(USD)</uni-th>
					<uni-th width="50" align="center">40HQ<br>(USD)</uni-th>
					<uni-th width="50" align="center">截关</uni-th>
					<uni-th width="50" align="center">操作</uni-th>
				</uni-tr>
				<uni-tr v-for="(item,index) in pricelist" :key="index" v-if="pricelist.length > 0 && isread">
					<uni-td align="center">
						<text v-if="item.ispush" class="text-red">
							<u-icon name="../../static/icon/flag.png" :size="25" />
						</text>
						{{ item.shipping }}
					</uni-td>
					<uni-td style="color: #ce3c3c;" align="center">{{ item.cost20 }} </uni-td>
					<uni-td style="color: #ce3c3c;" align="center">{{ item.cost40gp }}</uni-td>
					<uni-td style="color: #ce3c3c;" align="center">{{ item.cost40hq }}</uni-td>
					<uni-td align="center">{{ item.schedule }}</uni-td>
					<uni-td align="center">
						<button type="primary" size="mini" @click="checkDetail(item)">详情</button>
					</uni-td>
				</uni-tr>
			</uni-table>
		</block>
		<block v-if="pricelist.length <= 0 && isread">
			<view class=" bg-white m-1 px-2 rounded-half py-2 font-sm">
				<view class="flex justify-center" style="justify-content: space-between;">
					没有查询到运价<br>
					我们会尽快更新运价!!!
					<text style="display: flex;align-items: center;">
						<button type="primary" size="mini" @click="backToNext()">询盘</button>
					</text>
				</view>
			</view>
		</block>
	</view>
</template>

<script>
	import watermarkConfig from '../../common/free-lib/directives.js'
	export default {
		data() {
			return {
				isread: false,
				userInfo: {},
				datatemp: {},
				watermarkConfig: {
					text: '中集世倡0001',
					font: '12px 微软雅黑',
					textColor: '#dcdfe6',
					width: 210, //水印文字的水平间距
					height: 110 //水印文字的高度间距（低于文字高度会被替代）
				},
				pricelist: [],
				feelist: {},
			}
		},
		created() {
			let islogin = uni.getStorageSync('islogin')
			let user = uni.getStorageSync('dd_user')
			if (islogin && user) {
				this.watermarkConfig.text = user.data.data.name + user.data.data.mobile.substring(7, 11)
				uni.showLoading({
					title: '加载中',
					mask: true
				});
				let type = "";
				if (this.datatemp.pricetype.length == 3) {
					let p = this.datatemp.pricetype.join(',').split(",");
					type = "'" + p[0] + "'," + "'" + p[1] + "'," + "'" + p[2] + "'";
				} else {
					type = "'" + this.datatemp.pricetype.join(',').replace(",", "','") + "'";
				}
				this.$H.get('/so/price?method=fcllist&pol=' + this.datatemp.pol + '&pod=' +
					this.datatemp.pod + '&crrier=' + this.datatemp.carrier + '&pricetype=' + type, {}, {
						'content-type': 'text/html;charset=utf-8',
					}).then(res => {
					this.isread = true
					setTimeout(function() {
						uni.hideLoading();
					}, 300);
					if (res.data.length > 0) {
						this.pricelist = res.data.splice(0, 25);
					} else {
						this.pricelist = []
					}
				}).catch(res => {
					uni.showToast({
						title: '失败：' + res.message,
						icon: 'none'
					});
				})
			} else {
				uni.reLaunch({
					url: '/pages/price/error'
				});
			}
		},
		methods: {
			backToNext: function() {
				uni.navigateBack({
					delta: 1
				})
			},
			submitBook: function(item) {
				uni.setStorageSync("booking", item)
				uni.navigateTo({
					url: '/pages/price/booking',
					fail: (res) => {
						console.log(res) //打印错误信息
					}
				});
			},
			timeFormat: function(val) {
				let time = val.split('-')
				return time[0] + '/' + time[1] + '/' + time[2];
			},
			startType: function(val) {
				if (val == 'CLS') {
					return '大船截关'
				} else if (val == 'BETD') {
					return '大船驳船ON BOARD'
				} else if (val == 'ETD') {
					return '大船ON BOARD'
				} else if (val == 'TDETD') {
					return '提单ON BOARD'
				} else if (val == 'BCETD') {
					return '驳船ON BOARD'
				} else if (val == 'ONBOARD') {
					return '驳船ON BOARD'
				} else if (val == 'SOETD') {
					return 'SO ETD'
				} else if (val == 'GATE') {
					return 'GATE IN'
				} else {
					return ''
				}
			},
			checkDetail(val) {
				uni.setStorageSync("detail", val)
				uni.navigateTo({
					url: '/pages/price/detail',
					fail: (res) => {
						console.log(res) //打印错误信息
					}
				});
			},
			onLoad: function(option) {
				this.datatemp = uni.getStorageSync("bosslist_detail")
				if (!this.datatemp) {
					uni.showToast({
						title: '请输入起运港-目的港口查询',
						icon: 'none'
					});
					uni.navigateTo({
						url: '/pages/price/index',
						fail: (res) => {
							console.log(res) //打印错误信息
						}
					});
				}
			},
		},
	}
</script>

<style>
	>>>.uni-table-td {
		padding: 5px 0px;
	}

	>>>.uni-table-th {
		padding: 2px 0px;
	}

	>>>.uni-table-th-content {
		font-size: xx-small;
	}

	>>>uni-button {
		display: inline-flex;
		line-height: 2.3;
		font-size: 10px;
	}

	>>>.uni-table {
		background-color: initial;
	}

	>>>.table--stripe .uni-table-tr:nth-child(2n + 3) {
		background-color: inherit;
	}
</style>
