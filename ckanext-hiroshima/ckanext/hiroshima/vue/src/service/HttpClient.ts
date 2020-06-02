import axios from 'axios'

export default {
  namespaced: true,

  /**
   * Apiにgetリクエストを投げる
   * @param {String} url
   * @param {Object} params
   */
  get: (url: string, params: object) => {
    return axios.get(url, { params: params })
  },

  /**
   * Apiにヘッダ付きのgetリクエストを投げる
   */
  getAddHeader: async (url: string) => {
    const { data } = await axios.get(url)
    return data
  },
}
