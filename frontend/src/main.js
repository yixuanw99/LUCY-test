import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

// 如果你有其他的全局配置,可以在這裡添加
app.use(router)

app.mount('#app')
