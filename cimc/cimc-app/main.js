import Vue from 'vue'
import App from './App'
import store from './store';


Vue.prototype.$store = store
Vue.config.productionTip = false
import uView from "uview-ui";
Vue.use(uView);
App.mpType = 'app'


// 引入request库
import $H from '@/common/free-lib/request.js';
Vue.prototype.$H = $H
// 助手函数
import $U from './common/free-lib/util.js';
Vue.prototype.$U = $U

import i18n from './lang/index'
Vue.prototype._i18n = i18n

const app = new Vue({
	store,
	i18n,
	...App
})
app.$mount()
