<template>
	<view>
		<view class="wrap" style="margin: 130rpx 50rpx;">
			<u-grid :col="2" :border="false" style="font-weight: bold;">
				<u-grid-item>
					<navigator hover-class="none" url="../price/index">
						<u-icon name="../../static/img/jiaofuzongdan.png" :size="130"></u-icon>
						<view class="grid-text">运价查询</view>
					</navigator>
				</u-grid-item>
				<u-grid-item @click="notAvail">
					<navigator hover-class="none" url="../track/submitList">
						<u-icon name="../../static/img/ship.png" :size="130"></u-icon>
						<view class="grid-text">货物跟踪</view>
					</navigator>
				</u-grid-item>
				<u-grid-item @click="notAvail">
					<navigator hover-class="none">
						<u-icon name="../../static/tabIcon/hones1.png" :size="130"></u-icon>
						<view class="grid-text">入库确认</view>
					</navigator>
				</u-grid-item>
			</u-grid>
		</view>



	</view>
</template>

<script>
	export default {
		data() {
			return {

			}
		},
		created() {
			this.$U.setStorage('url', 'http://47.112.190.46:81');
		},
		methods: {
			notAvail() {
				uni.showToast({
					title: "该功能暂未开通",
					icon: 'none'
				})
			},
			openLogin() {
				uni.navigateTo({
					url: '../login/login',
				});

			},
		}
	}
</script>

<style lang="scss" scoped>
	.status_bar {
		//height: var(--status-bar-height);
		//width: 100%;
	}

	.wrap {
		padding: 24rpx;
	}

	.u-row {
		margin: 40rpx 0;
	}

	.demo-layout {
		height: 80rpx;
		border-radius: 8rpx;
	}

	.bg-purple {
		background: #d3dce6;
	}

	.bg-purple-light {
		background: #e5e9f2;
	}

	.bg-purple-dark {
		background: #99a9bf;
	}
</style>
