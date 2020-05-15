import Vue from 'vue'
import App from '../App.vue'
import router from './router'

import {Menu, Layout} from 'ant-design-vue'


Vue.config.productionTip = false
Vue.use(Menu)
Vue.use(Layout)
new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
