import axios from "axios";
import router from "@/router";

export const axiosClient = axios.create({
  baseURL: 'http://fastapi_backend:8000',
  timeout: 1000
})

axiosClient.interceptors.response.use((res) => res, (err) => {
  switch (err.response.status) {
    case 403:
      router.push('/login/')
      break
    case 401:
      return Promise.reject(err)
    case 404:
      return Promise.reject(err)
    case 422:
      return Promise.reject(err)
    default:
      console.log('Unknown StatusCode -> ' + err.response.status)
  }
})
