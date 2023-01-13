import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RepositoryView from '@/views/RepositoryView.vue'
import LoginView from '@/views/LoginView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import {useTokenStore} from "@/store/token";

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
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFoundView',
    component: NotFoundView
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

const publicPages = ['/login'];

router.beforeEach((to, from, next) => {

  const authRequired = !publicPages.includes((to.path))
  const loggedIn = useTokenStore().token
  console.log("beforeEach -> " + loggedIn)

  if (authRequired && !loggedIn) {
    next('/login')
  } else if(to.path === '/login' && loggedIn ){
    next('/')
  } else {
    next()
  }
})

export default router
