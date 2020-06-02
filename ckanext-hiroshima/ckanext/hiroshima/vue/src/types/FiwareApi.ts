export interface FiwareResponse {
  contextResponses: ContextResponses[]
}

interface ContextResponses {
  contextElement: ContextElement
  statusCode: {
    code: string
    reasonPhrase: string
  }
}

interface ContextElement {
  attributes: Attributes[]
  id: string
  isPattern: boolean
  type: string
}

interface Attributes {
  name: string
  values: Entities[]
}

interface Entities {
  recvTime: string
  attrType: string
  attrValue: string
}