<template>
	<view class="card-content">
		<view class="view-content">
			<view style="text-align: center; padding: 20rpx">
				<text class="title-text">FCL报价查询</text>
			</view>
			<view style="border-bottom: 1px solid #e5e5e5; margin-bottom: 40rpx" />
			<view style="padding: 0px 20px 40px">
				<uni-forms :value="formData">
					<uni-forms-item name="pol" label="起运港">
						<input v-model="formData.pol" type="text" placeholder="请输入起运港" @click="openStartPage(0)" />
					</uni-forms-item>
					<uni-forms-item name="pod" label="目的港">
						<input v-model="formData.pod" type="text" placeholder="请输入目的港" @click="openStartPage(1)" />
					</uni-forms-item>
					<uni-forms-item name="carrier" label="船公司">
						<input adjust-position="false" autocomplete="off" @focus="focus" auto-blur="false"
							v-model="formData.carrier" type="text" placeholder="请选择船公司" @click="openCarrierList()" />
					</uni-forms-item>
					<uni-forms-item name="freight" label="运价类型">
						<uni-data-checkbox multiple v-model="formData.pricetype" :localdata="freightlist" />
					</uni-forms-item>
					<uni-forms-item name="mode" label="查询模式">
						<uni-data-checkbox v-model="mode" :localdata="modedata" />
					</uni-forms-item>
				</uni-forms>
				<button type="primary" @click="submitForm">立即查询</button>
			</view>
		</view>
		<uni-popup ref="carrierPopup" type="bottom" mask-background-color="rgba(0,0,0,-0.6)">
			<scroll-view scroll-y="true" class="scroll-Y">
				<view class="popup-view" v-for="(item, index) in carrierlist" @click="bindCarrierChange(item.name)">
					<text>{{ item.name }}</text>
				</view>
			</scroll-view>
		</uni-popup>
	</view>
</template>

<script>
	import * as dd from "dingtalk-jsapi";

	export default {
		data() {
			return {
				mode: 0,
				keyword: "",
				carrierlist: [],
				isHideKeyboard: true,
				formData: {
					pol: "",
					pod: "",
					carrier: "",
					date: Date.now(),
					pricetype: ["FAK", "NAC", "SPOT"],
				},
				modedata: [{
						value: 0,
						text: "模式一",
					},
					{
						value: 1,
						text: "模式二",
					},
				],
				freightlist: [{
						value: "FAK",
						text: "FAK",
					},
					{
						value: "NAC",
						text: "NAC",
					},
					{
						value: "SPOT",
						text: "SPOT",
					},
				],
			};
		},
		methods: {
			/**
			 * 禁止软键盘弹出
			 */
			focus() {
				if (this.isHideKeyboard) uni.hideKeyboard();
			},

			/**
			 * 船公司列表
			 * @param {Object} e
			 */
			openCarrierList: async function(e) {
				this.$refs.carrierPopup.open("bottom");
				this.$H
					.post("/so/combobox?method=fscarrier", this.form, {})
					.then((res) => {
						this.carrierlist = res;
					})
					.catch((res) => {
						console.log(res);
						uni.showToast({
							title: "失败：" + res.message,
							icon: "none",
						});
					});
			},

			/**
			 * 选择船公司
			 * @param {Object} e
			 */
			bindCarrierChange: function(e) {
				this.formData.carrier = e;
				this.$refs.carrierPopup.close();
			},

			/**
			 * 港口搜索
			 * @param {Object} val
			 */
			openStartPage: function(val) {
				uni.navigateTo({
					url: "/pages/price/search?id=" + val,
					fail: (res) => {
						console.log(res); //打印错误信息
					},
				});
			},

			/**
			 * 查询运价
			 */
			submitForm() {
				let bRet = uni.getStorageSync("isAvailable");
				if (!bRet) {
					uni.showToast({
						title: "网络错误！请重新登录或刷新页面",
						icon: "none",
					});
					return;
				}
				if (this.formData.pol == "" || this.formData.pod == "") {
					uni.showToast({
						title: "请输入港口查询",
						icon: "none",
					});
					return;
				}
				if (this.mode == 0) {
					uni.setStorageSync("bosslist_detail", this.formData);
					uni.navigateTo({
						url: "/pages/price/bosslist",
						fail: (res) => {
							console.log(res);
						},
					});
				} else {
					uni.setStorageSync("list_detail", this.formData);
					uni.navigateTo({
						url: "/pages/price/list",
						fail: (res) => {
							console.log(res);
						},
					});
				}
			},

			/**
			 * 钉钉授权
			 */
			loginDD() {
				dd.ready(function() {
					dd.runtime.permission.requestAuthCode({
						corpId: "ding2bb9458351f19b9b35c2f4657eb6378f",
						onSuccess: function(result) {
							uni.setStorageSync("code", result.code);
							console.log("code", result.code);
							uni.request({
								url: "http://47.112.190.46/login",
								data: {
									authCode: uni.getStorageSync("code"),
								},
								method: "GET",
								success: (res) => {
									if (!res.data.success) {
										uni.showToast({
											title: "钉钉未授权，<br/>没有调用该接口的权限",
											icon: "none",
										});
										return;
									}
									uni.setStorageSync("dd_user", res);
									uni.setStorageSync("islogin", true);
								},
								fail: (res) => {
									uni.reLaunch({
										url: "/pages/price/error",
									});
								},
							});
						},
						onFail: function(err) {
							uni.reLaunch({
								url: "/pages/price/error",
							});
						},
					});
				});
			},
		},

		/**
		 * 获取搜索港口返回值
		 */
		onShow() {
			let pages = getCurrentPages();
			let currPage = pages[pages.length - 1]; // 当前页的实例
			if (currPage.$vm.index) {
				if (currPage.$vm.index.id == 0) {
					this.formData.pol = currPage.$vm.value;
				} else {
					this.formData.pod = currPage.$vm.value;
				}
			}
		},

		/**
		 * 生命周期-创建时
		 */
		created() {
			//TODO 后续添加到拦截器中
			uni.removeStorageSync("isAvailable");
			uni.removeStorageSync("dd_user");
			uni.removeStorageSync("code");

			//测试使用
			// uni.setStorageSync('islogin', true)
			// uni.setStorageSync('dd_user', {
			// 	data: {
			// 		data: {
			// 			"name": "梁文辉",
			// 			"mobile": "13267690653"
			// 		}
			// 	}
			// })

			this.loginDD();

			uni.showLoading({
				title: "加载中",
				mask: true,
			});

			setTimeout(function() {
				let islogin = uni.getStorageSync("islogin");
				if (islogin) {
					uni.request({
						url: "http://47.112.190.46:81/so/login?method=loginapp",
						data: {
							username: "梁文辉",
							issysuser: "on",
						},
						method: "POST",
						success: (res) => {
							if (!res.data.success) {
								uni.showToast({
									title: res.data.message,
									icon: "none",
								});
								return;
							}
							uni.setStorageSync("isAvailable", true);
							uni.hideLoading();
						},
						fail: (res) => {
							uni.showToast({
								title: "失败：" + res.message,
								icon: "none",
							});
						},
					});
				} else {
					uni.reLaunch({
						url: "/pages/price/error",
					});
				}
			}, 1250);
		},
	};
</script>

<style scoped>
	.card-content {
		height: calc(100vh);
		background-color: #62a3e3;
		background-image: url(@/static/img/bg.png);
		background-repeat: no-repeat;
		/* 图片按比例显示，其余部分为其他颜色 */
		background-size: contain;
		/*图片等比例缩放*/
		overflow-y: auto;
	}

	.view-content {
		margin: 110px 14px;
		background-color: #ffffff;
		box-shadow: rgb(0 0 0 / 15%) 0px 0px 3px 1px;
		border-radius: 15px;
		height: calc(100vh - 33vh);
	}

	.title-text {
		font-size: x-large;
		font-weight: 800;
		flex: 1;
		color: #333;
	}

	>>>.uni-input-placeholder {
		font-size: small;
	}

	>>>.uni-forms-item__inner {
		align-items: baseline;
	}

	>>>.uni-forms-item__inner {
		padding-bottom: 12px;
	}

	.scroll-Y {
		width: 100%;
		height: calc(100vh - 51vh);
		background-color: #ffffff;
		border-top-left-radius: 15px;
		border-top-right-radius: 15px;
	}

	.popup-view {
		text-align: center;
		margin: 30rpx;
	}

	>>>.uni-data-checklist .checklist-group {
		flex-wrap: inherit;
	}
</style>
