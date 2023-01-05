import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'

export const useTokenStore = defineStore({
  id: 'token',
  state: () => ({
    token: useStorage('token', null)
  })
})
