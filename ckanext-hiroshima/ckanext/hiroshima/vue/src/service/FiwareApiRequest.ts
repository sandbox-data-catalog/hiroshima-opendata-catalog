import HttpClient from './HttpClient'
import { FiwareResponse } from '@/types/FiwareApi'

export default {
  namespaced: true,

  /**
   * IoT連携グラフの集計（折れ線グラフ）
   */
  getDatasetNumPerLine: async (
    entityType: string,
    entityId: string,
    attrName: string
  ): Promise<FiwareResponse> => {
    const getUrl = '/fiware/' + entityType + '/' + entityId + '/' + attrName
    const data = await HttpClient.getAddHeader(getUrl)
    return data
  },
}
