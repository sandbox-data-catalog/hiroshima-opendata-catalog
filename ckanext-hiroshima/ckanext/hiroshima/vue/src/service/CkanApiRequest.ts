import HttpClient from './HttpClient'

import { PackageShowResultResponse } from '@/types/CkanApi'

export default {
  namespaced: true,

  /**
   * 指定idのランキング取得処理
   *
   * @param ids
   */
  getViewRankingListIncludeAccessCount: async (
    ids: string[]
  ): Promise<PackageShowResultResponse[]> => {
    const actionList = ids.map((id) => {
      return HttpClient.get('/api/3/action/package_show', {
        id,
        include_tracking: true,
      })
    })
    const data = await Promise.all(actionList)
    return data.map(({ data }) => data.result)
  },

  /**
   * 組織ごとのデータセット情報を取得
   */
  getDatasetByOrganization: async () => {
    const { data } = await HttpClient.get(
      '/api/3/action/package_search?facet.field=["organization"]&rows=0',
      {}
    )
    return data.result
  },

  /**
   * グループごとのデータセット情報を取得
   */
  getDatasetByGroup: async () => {
    const { data } = await HttpClient.get(
      '/api/3/action/package_search?facet.field=["groups"]&rows=0',
      {}
    )
    return data.result
  },

  /**
   * タグごとのデータセット情報を取得
   */
  getDatasetByTag: async () => {
    const { data } = await HttpClient.get(
      '/api/3/action/package_search?facet.field=["tags"]&rows=0',
      {}
    )
    return data.result
  },
}
