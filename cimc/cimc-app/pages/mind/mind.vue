<template>
	<view>
		<view class="" style="height: 350rpx;background-color: #6DBA52;padding: 50rpx; box-sizing: border-box;">
			<view class="u-f u-f-ac" style="width: 70%;">
				<image style="background-color: #fff; margin: 30rpx; border-radius: 50%; 
				height: 160rpx;width: 160rpx;" src="../../static/img/ship.png"></image>
				<view class="" style="margin-left: 40rpx; font-weight: bold;color: #fff;">
					<view class="">
						<text style="font-size: 55rpx;">
							{{userInfo.username ? userInfo.username : '未登录'}}
						</text>
					</view>
					<view class="">
						<text style="font-size: 33rpx;">
						</text>
					</view>
				</view>
			</view>
		</view>
		<!-- List -->
		<view class="">
			<block v-for="(item,index) in list" :key="index">
				<view @click="notAvail(index)" class="u-f u-f-jsb"
					style="margin: 15rpx 50rpx;border-bottom: 1px solid #eee;padding-bottom: 20rpx; ">
					<view class="u-f">
						<u-icon style="color: #6DBA52;margin-right: 30rpx;" :name="item.icon" size="48"></u-icon>
						<view class="" style="height: 48rpx;">
							<text style="font-weight: bold;font-size: 30rpx;">{{item.name}}</text>
						</view>
					</view>
					<u-icon style="color: #999;font-size: 300;" name="arrow-right" size="38"></u-icon>
				</view>
			</block>
			<view @click="changeLang" class="u-f u-f-jsb"
				style="margin: 15rpx 50rpx;border-bottom: 1px solid #eee;padding-bottom: 20rpx; ">
				<view class="u-f">
					<u-icon style="color: #6DBA52;margin-right: 30rpx;" name="order" size="48"></u-icon>
					<view class="" style="height: 48rpx;">
						<text style="font-weight: bold;font-size: 30rpx;">切换语言</text>
					</view>
				</view>
				<u-icon style="color: #999;font-size: 300;" name="arrow-right" size="38"></u-icon>
			</view>
		</view>

		<!-- 密码修改弹窗 -->
		<u-popup v-model="showPop" mode="bottom" border-radius="20">
			<view class="px-3">
				<view class="flex justify-between align-center">
					<text class="font-weight-bold">修改密码</text>
					<text @click="showPop = false" class="iconfont icon-reeor  "
						style="font-size: 56rpx;color: #6DBA52;"></text>
				</view>
				<view class="flex justify-center align-center">
					<text class="iconfont icon-unlock mr-2 " style="font-size: 56rpx;color: #6DBA52;"></text>
					<input type="text" v-model="pwd.userpwd" placeholder="请输入原密码" class="border-bottom"
						style="border-color: #6DBA52;" value="" />
				</view>
				<view class="flex justify-center align-center">
					<text class="iconfont icon-password1  mr-2 " style="font-size: 56rpx;color: #6DBA52;"></text>
					<input type="text" v-model="pwd.newciphertext" placeholder="请输入新密码" class="border-bottom"
						style="border-color: #6DBA52;" value="" />
				</view>
				<view class="flex justify-center align-center">
					<text class="iconfont icon-password1  mr-2 " style="font-size: 56rpx;color: #6DBA52;"></text>
					<input type="text" v-model="pwd.newsecretkey" placeholder="请再次输入新密码" class="border-bottom"
						style="border-color: #6DBA52;" value="" />
				</view>
				<view class="bg-primary rounded-20 flex justify-center text-white font-lg mb-5 mt-3 "
					@click="changePwd">确 定</view>
			</view>
		</u-popup>
		<!-- 外层 -->
	</view>
</template>

<script>
	export default {
		data() {
			return {
				pwd: {
					userpwd: '123',
					newciphertext: '123',
					newsecretkey: '123',
					username: 'CIMC',
					action: 'updatePwd',
					timeStamp: '3',
					apiKey: 'test-api-key',
					source: 'android',
					appVersion: 'v1.1.0',
					timeStamp: new Date().getTime()
				},
				showPop: false,
				userInfo: {},
				list: [{
						icon: 'setting',
						name: '应用设置'
					},
					{
						icon: 'lock',
						name: '修改密码'
					},
					{
						icon: 'android-circle-fill',
						name: '版本更新'
					},
					{
						icon: 'info-circle',
						name: '退出'
					}, {
						icon: 'server-man',
						name: '帮助'
					},

				],
				dataList: [{
					id: "1",
					name: 'A'
				}, {
					id: "2",
					name: 'B'
				}, {
					id: "3",
					name: 'C'
				}]
			}
		},
		onLoad() {},
		created() {
			// this.userInfo = JSON.parse(this.$U.getStorage('dd_user'))
			// this.pwd.token = this.userInfo.token
			// console.log(this.userInfo)
			// if (!this.userInfo.username) {
			// 	this.userInfo.username = '未登录'
			// }
		},
		methods: {
			changePwd() {
				if (!this.pwd.userpwd || !this.pwd.newciphertext || !this.pwd.newsecretkey) {
					uni.showToast({
						title: '原密码或新密码不能为空',
						icon: "none"
					});
					return
				}
				if (!(this.pwd.newciphertext === this.pwd.newsecretkey)) {
					uni.showToast({
						title: '新密码和确认密码不一致',
						icon: "none"
					});
					return
				}
				console.log(this.pwd)
				this.userInfo = JSON.parse(this.$U.getStorage('user'))
				this.pwd.token = this.userInfo.token
				this.pwd.timeStamp = new Date().getTime()
				this.$H.post('/user', this.pwd, {
					token: false
				}).then(res => {
					// 登录
					uni.showToast({
						title: res.message,
						icon: 'none'
					});
					if (res.code === '0000') {
						setTimeout((res) => {
							uni.navigateTo({
								url: '../login/login'
							});
							this.pwd.userpwd = ''
							this.pwd.newciphertext = ''
							this.pwd.newsecretkey = ''
						}, 1500);
					}
				}).catch(res => {
					uni.showToast({
						title: '错误' + res.statusCode,
						icon: 'none'
					});

				})
			},
			notAvail(index) {
				switch (index) {
					case 0:
						uni.showToast({
							title: "该功能暂未开通",
							icon: 'none'
						})
						break;
					case 1:
						this.showPop = true
						break;
					case 2:
						this.$U.update()
					case 3:
						uni.navigateTo({
							url: '../login/login'
						})
						uni.showToast({
							title: "退出成功",
							icon: 'none'
						})
						this.$U.removeStorage('user')
						break;
					case 4:
						uni.showToast({
							title: "该功能暂未开通",
							icon: 'none'
						})
						break;
					default:
						uni.showToast({
							title: "该功能暂未开通",
							icon: 'none'
						})
						break;
				}
			},
			changeLang() {
				uni.showToast({
					title: '切'
				});
			}
		}
	}
</script>

<style>

</style>
