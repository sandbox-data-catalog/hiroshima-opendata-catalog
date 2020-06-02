export interface PackageSearchResponse {
  count: number
  search_facets: SearchFacets
  sort: string
  results: PackageSearchResultResponse[]
}

export interface PackageSearchResultResponse {
  author?: string
  author_email?: string
  creator_user_id?: string
  id: string
  isopen: boolean
  license_id: string
  license_title: string
  license_url: string
  maintainer?: string
  maintainer_email?: string
  metadata_created: string
  metadata_modified: string
  name: string
  notes?: string
  num_resources: number
  num_tags: number
  organization?: string
  owner_org?: string
  private: boolean
  revision_id: string
  state: string
  title: string
  type: string
  url?: string
  version?: number
  tags: PackageSearchResultTags[]
  groups: PackageSearchResultGroups[]
  // TODO: 記載漏れている内容は適宜型を追記
}

export interface PackageShowResultResponse {
  author?: string
  author_email?: string
  creator_user_id?: string
  id: string
  isopen: boolean
  license_id: string
  license_title: string
  license_url: string
  maintainer?: string
  maintainer_email?: string
  metadata_created: string
  metadata_modified: string
  name: string
  notes?: string
  num_resources: number
  num_tags: number
  organization?: string
  owner_org?: string
  private: boolean
  revision_id: string
  state: string
  title: string
  type: string
  url?: string
  version?: number
  tracking_summary: {
    total: number
    recent: number
  }
  tags: PackageSearchResultTags[]
  groups: PackageSearchResultGroups[]
  // TODO: 記載漏れている内容は適宜型を追記
}

export interface PackageSearchResultTags {
  display_name: string
  id: string
  name: string
  state?: string
  vocabulary_id?: string
  count?: number
}

interface PackageSearchResultGroups {
  description: string
  display_name: string
  id: string
  name: string
  image_display_url: string
  title: string
}

interface SearchFacets {
  tags :Tags
}

interface Tags {
  items : PackageSearchResultTags[]
}