<template>
	<view class="card-content">
		<view style="height: 100rpx;">
			<uni-search-bar confirm-type="search" radius="15" @confirm="search" v-model="keyword" @cancel="cancal"
				:adjust-position="false">
			</uni-search-bar>
		</view>

		<view style="height: 240rpx;">
			<view>
				<uni-nav-bar backgroundColor="#f5f5f5" leftText="历史港口" right-icon="trash-filled"
					@clickRight="clearHistory" />
			</view>
			<view class="view-body">
				<view class="example-body-item" v-for="(item,index) in citylist">
					<view @click="selectMode(item.value,index)">{{item.name}}</view>
				</view>
			</view>
		</view>
		<view style="border-bottom: 1px solid #e5e5e5;" />
		<uni-indexed-list :options="list" :show-select="false" @click="bindClick" />

		<!-- 弹窗 -->
		<uni-popup ref="popup" type="bottom" mask-background-color="rgba(0,0,0,-0.6)" backgroundColor="#FFFFFF">
			<view class="" style="height: calc(100vh - 103rpx);overflow-y: auto;">
				<uni-list v-for="(item,index) in portlist" index="index">
					<uni-list-item :title="item.namee +' / '+ item.namec" @click="searchport(item)" clickable />
				</uni-list>
			</view>
		</uni-popup>
	</view>
</template>


<script>
	export default {
		data() {
			return {
				index: '',
				keyword: '',
				portlist: [],
				list: [{
					'letter': 'A',
					'data': []
				}],
				citylist: [{
					'value': 'SHENZHEN',
					'name': '深圳'
				}]
			}
		},
		created() {
			if (uni.getStorageSync("search_key")) {
				this.citylist = uni.getStorageSync("search_key")
			}
		},
		methods: {
			clearHistory() {
				uni.removeStorageSync("search_key")
				this.citylist = []
			},
			search(val) {
				this.$refs.popup.open('bottom')
				if (this.index.id == 0) {
					this.$H.get('/scp/service?src=flexbox&action=fclpol&q=' + val.value +
						'&p=1&s=50', {}, {}).then(res => {
						this.portlist = res.results
					}).catch(res => {
						uni.showToast({
							title: '失败：' + res.message,
							icon: 'none'
						});
					})
				} else {
					this.$H.post('/scp/service?src=flexbox&action=fclpod&q=' + val.value +
						'&p=1&s=50', {}, {}).then(res => {
						this.portlist = res.results
					}).catch(res => {
						uni.showToast({
							title: '失败：' + res.message,
							icon: 'none'
						});
					})
				}
			},
			cancal() {
				this.$refs.popup.close()
			},
			/**
			 * 查询港口地址
			 */
			searchport(e) {
				let obj = {}
				obj['value'] = e.namee;
				obj['name'] = e.namec;
				let temp = 0;

				for (var i = 0; i < this.citylist.length; i++) {
					if (this.citylist[i].name == e.namec) {
						temp++;
					}
				}
				if (temp == 0 && this.citylist.length <= 8) {
					if (this.citylist.length == 8) {
						this.citylist.pop()
						this.citylist.push(obj)
						uni.setStorageSync('search_key', this.citylist);
					} else {
						this.citylist.push(obj)
						uni.setStorageSync('search_key', this.citylist);
					}
				}

				this.$refs.popup.close()
				let pages = getCurrentPages()
				let nowPage = pages[pages.length - 1]; //当前页页面实例
				let prevPage = pages[pages.length - 2]; //上一页页面实例
				prevPage.$vm.index = this.index
				prevPage.$vm.value = e.namee
				uni.navigateBack({
					delta: 1,
				});
			},
			bindClick(e) {
				var str = e.item.name.split('/');
				let pages = getCurrentPages()
				let nowPage = pages[pages.length - 1]; //当前页页面实例
				let prevPage = pages[pages.length - 2]; //上一页页面实例
				prevPage.$vm.index = this.index
				prevPage.$vm.value = str[0].trim()
				uni.navigateBack({
					delta: 1,
				});
			},
			selectMode(val) {
				let pages = getCurrentPages()
				let nowPage = pages[pages.length - 1]; //当前页页面实例
				let prevPage = pages[pages.length - 2]; //上一页页面实例
				prevPage.$vm.index = this.index
				prevPage.$vm.value = val
				uni.navigateBack({
					delta: 1,
				});
			},
			onLoad: function(option) {
				this.index = option
				let isRet = uni.getStorageSync("portlist")
				if (isRet) {
					this.list = isRet
				} else {
					this.$H.post('/scp/service?src=flexbox&action=fclpod&q=&p=1&s=500', {}, {}).then(res => {
						var list_map = new Array();
						var data = res.results
						for (var i = 0; i < data.length; i++) {
							list_map.push({
								letter: data[i].namee.substr(0, 1),
								data: []
							});
						}
						//res去重复后的集合
						var res = [];
						var temp = {};
						for (var i = 0; i < list_map.length; i++) {
							if (!temp[list_map[i].letter]) {
								res.push(list_map[i]);
								temp[list_map[i].letter] = 1;
							}
						}
						// abc顺序排序
						for (var i = 0; i < res.length; i++) {
							for (var j = i + 1; j < res.length; j++) {
								//如果第一个比第二个大，就交换他们两个位置
								if (res[i].letter.charCodeAt() > res[j].letter.charCodeAt()) {
									var temp = res[i];
									res[i] = res[j];
									res[j] = temp;
								}
							}
						}
						for (var i = 0; i < res.length; i++) {
							for (var j = 0; j < data.length; j++) {
								if (res[i].letter == data[j].namee.substr(0, 1)) {
									res[i].data.push(data[j].namee + ' / ' + data[j].namec)
								}
							}
						}
						this.list = res
						uni.setStorageSync("portlist", this.list)
					}).catch(res => {
						uni.showToast({
							title: '失败：' + res.message,
							icon: 'none'
						});
					})
				}
			}
		},

	}
</script>

<style scoped>
	.card-content {
		height: calc(100vh);
	}

	uni-view {
		font-size: 12px;
	}

	.search-result-text {
		text-align: center;
		font-size: 14px;
		color: #666;
	}

	>>>.uni-indexed-list {
		top: 345rpx;
	}

	.example-body {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: row;
		padding: 20rpx;
	}

	>>>.uni-popup {
		top: 47px;
	}

	>>>.uni-icons {
		font-size: 20px !important;
	}

	.view-body {
		display: flex;
		flex-wrap: wrap;
		margin-top: 5px;
		margin-left: 5px;
	}

	.example-body-item {
		border-color: #e5e5e5;
		border-style: solid;
		border-width: 1px;
		border-radius: 15px;
		text-align: center;
		width: 80px;
		margin: 3px 3px;
	}

	>>>.uni-transition {
		background-color: rgb(255 255 255);
		margin-top: 55px;
	}

	>>>.uni-navbar__header-btns-left {
		padding-left: 20px;
	}
</style>
