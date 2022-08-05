<template>
	<view style="background: #eee;height: 100%;">
		<view class="">
			<view style="background: #6DBA52;
						height: 240rpx" class="">

			</view>

			<view class="card">
				<slot></slot>
			</view>

			<view class="">
				<slot name="outside"></slot>
			</view>
		</view>
	</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {

			}
		},
		methods: {

		}
	}
</script>

<style scoped lang="scss">
	page {
		height: 100%;
	}

	.card {
		height: 30%;
		background: #fff;
		margin: 0 20rpx;
		position: relative;
		border-radius: 30rpx;
		top: -140rpx;
		padding: 20rpx;
	}
</style>
