<template>
	<view>
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<view class="">
			<button class="changeBtn" type="primary" @click="change">{{i18n.change}}</button>
			<!-- <button class="configBtn" type="primary" @click="config">配置</button> -->
		</view>

		<view class="" style="margin: 100rpx;margin-top: 220rpx;">
			<u-image width="100%" height="200rpx" mode="widthFix" :src="i18n.logo" style="margin-bottom: 90rpx;">
			</u-image>

			<view class="" style="border-bottom: 1rpx solid #eee;">
				<text>{{i18n.name}}</text>
				<u-input :placeholder="i18n.namehoder" v-model="form.username" />
			</view>

			<view class="" style="border-bottom: 1rpx solid #eee;">
				<text>{{i18n.pwd}}</text>
				<u-input :placeholder="i18n.pwdhoder" v-model="form.userpwd" type="password" />
			</view>

			<u-checkbox-group style="margin: 20rpx 0;">

				<u-checkbox @change="checkboxChange" v-model="form.issysuser" active-color="#6DBA52">{{i18n.issysuser}}
				</u-checkbox>
				<u-checkbox @change="checkboxChange" v-model="value" active-color="#6DBA52">{{i18n.rememberme}}
				</u-checkbox>
			</u-checkbox-group>

			<button @click="openLogin"
				style="margin-top: 80rpx; width: 60%; background-color: #6DBA52; border-radius: 66rpx;"
				type="primary">{{i18n.login}} </button>

		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				form: {
					username: 'LIANGWENHUI',
					action: 'login',
					userpwd: 'cimc@1234',
					source: 'android',
					appVersion: 'v1.1.0',
					sim: '1380013800',
					issysuser: true,
					timeStamp: new Date().getTime()

				},
				value: false,
				isLogin: false
			}
		},
		computed: {
			i18n() {
				return this.$t('login')
			}
		},
		// onBackPress(options) {
		// 	if (this.isLogin) {
		// 		return false
		// 	}
		// 	return true
		// },
		created() {
			let user = this.$U.getStorage('rememberMe')
			if (user) {
				user = JSON.parse(user)

				this.value = true
				this.form.username = user.name
				this.form.userpwd = user.pwd
				this.form.issysuser = user.issysuser
			} else {
				this.value = false
			}
			console.log(user + '----------------')
		},
		methods: {
			change() {
				console.log('语言切换')
				const system_info = uni.getStorageSync('system_info')
				system_info.language === 'en' ? system_info.language = this._i18n.locale = 'zh_CN' : system_info.language =
					this._i18n.locale = 'en'
				uni.setStorageSync('system_info', system_info)
				// uni.reLaunch({
				// 	url: 'index'
				// })
			},
			checkboxChange(e) {
				console.log(e);
				if (e) {
					if (!this.form.username | !this.form.userpwd) {
						uni.showToast({
							title: "账号或密码不能为空",
							icon: 'none'
						})
						this.value = false
						return
					}

					this.$U.setStorage('rememberMe', JSON.stringify({
						name: this.form.username,
						pwd: this.form.userpwd,
						issysuser: this.form.issysuser
					}))
					return
				}
				this.$U.removeStorage('rememberMe')
			},
			config() {
				uni.switchTab({
					url: "/pages/config/config"
				})
			},
			openLogin() {
				// console.log(this.form)

				if (!this.form.username | !this.form.userpwd) {
					uni.showToast({
						title: "账号或密码不能为空",
						icon: 'none'
					})
					return
				}

				this.form.timeStamp = new Date().getTime()
				this.$H.post('/login?method=login&type=app', this.form, {
					token: false
				}).then(res => {
					// 登录
					console.log(res)
					if (res.data) {
						this.$store.dispatch('login', res.data)
					}


					if (res.success === true) {
						uni.showToast({
							title: '登录成功'
						});
						if (this.value) {
							this.$U.setStorage('rememberMe', JSON.stringify({
								name: this.form.username,
								pwd: this.form.userpwd
							}))
						}


						setTimeout((res) => {
							uni.switchTab({
								url: "/pages/index/index"
							})
						}, 300);
						return
					}
					uni.showToast({
						title: '登录失败：' + res.message,
						icon: 'none'
					});

				}).catch(res => {
					console.log(res)
					uni.showToast({
						title: '登录失败2：' + res.message,
						icon: 'none'
					});
				})
				// this.$emit('changeLogin')
				// this.isLogin = true
				// setTimeout(function() {
				// 	uni.navigateBack({
				// 		delta: 1
				// 	})
				// }, 300);

			},
		}
	}
</script>

<style scoped lang="scss">
	.changeBtn {
		line-height: 60rpx;
		height: 60rpx;
		width: 140rpx;
		position: absolute;
		right: 5%;
		bottom: 37%;
		background-color: rgb(109, 186, 82);
	}

	.configBtn {
		line-height: 60rpx;
		height: 60rpx;
		width: 140rpx;
		position: absolute;
		right: 5%;
		bottom: 30%;
		background-color: rgb(109, 186, 82);
	}
</style>
