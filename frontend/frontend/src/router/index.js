import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import RepositoryView from '@/views/RepositoryView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/repository-view/:id',
    name: 'RepositoryView',
    component: RepositoryView,
    props: true
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router
