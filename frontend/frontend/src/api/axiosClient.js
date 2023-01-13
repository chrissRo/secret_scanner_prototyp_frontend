import axios from "axios";
import router from "@/router";

export const axiosClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 1000
})

axiosClient.interceptors.response.use((res) => res, (err) => {
  switch (err.response.status) {
    case 403:
      router.push('/login/')
      break
    default:
      console.log('Unknown StatusCode ->' + err.response.status)
  }
})
