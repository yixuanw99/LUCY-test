import { createRouter, createWebHistory } from 'vue-router'
import FetchReport from '@/views/FetchReport.vue'
import EpigeneticReport from '@/views/EpigeneticReport.vue'

const routes = [
  {
    path: '/',
    name: 'FetchReport',
    component: FetchReport
  },
  {
    path: '/report/:id',
    name: 'ReportDisplay',
    component: EpigeneticReport
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
