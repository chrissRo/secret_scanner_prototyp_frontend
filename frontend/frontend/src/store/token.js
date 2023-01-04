import {defineStore} from "pinia";
import {useStorage} from '@vueuse/core'

export const useTokenStore = defineStore({
  id: 'token',
  state: () => ({
    token: useStorage('token', null)
  }),
  actions: {
    async signIn(username, password) {
      // Todo api-call for login
      if(username === 'testUser' && password === 'testPassword!'){
        this.token = 'abcd123abcd123';
      }
    }
  }
})
