import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import RepositoryFindingView from '@/views/RepositoryFindingView.vue'
import LoginView from '@/views/LoginView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import FavouriteView from '@/views/FavouriteView.vue'
import TruePositiveView from '@/views/TruePositiveView.vue'
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
    path: '/repository-finding-view/:id/:lastScan',
    name: 'RepositoryFindingView',
    component: RepositoryFindingView,
    props: true,
    auth: true
  },
  {
    path: '/favourite-view',
    name: 'FavouriteView',
    component: FavouriteView,
    auth: true
  },
  {
    path: '/true-positive-view',
    name: 'TruePositiveView',
    component: TruePositiveView,
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

  if (authRequired && !loggedIn) {
    next('/login')
  } else if(to.path === '/login' && loggedIn ){
    next('/')

  } else {
    next()
  }
})

export default router
