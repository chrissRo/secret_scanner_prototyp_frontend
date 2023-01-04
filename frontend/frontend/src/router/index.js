import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RepositoryView from '@/views/RepositoryView.vue'
import LoginView from '@/views/LoginView'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/repository-view/:id',
    name: 'RepositoryView',
    component: RepositoryView,
    props: true,
    auth: true
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router
