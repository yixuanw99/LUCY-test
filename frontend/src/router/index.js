// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import EpigeneticReport from '@/views/EpigeneticReport.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: EpigeneticReport
  },
  // Add more routes as needed
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router