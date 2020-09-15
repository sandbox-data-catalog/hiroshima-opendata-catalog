<template>
  <div id="disp">
    <div id="container">
      <!-- コンテナ -->
      <div id="logo" class="column">
        <div id="top">
          <div>
            <span>ひろしま</span>
            <span>サンドボックス</span>
          </div>
        </div>
        <div id="logoimage" />
        <div id="bottom">
          <div>
            <span>データ</span>
            <span>カタログサイト</span>
          </div>
        </div>
      </div>
      <div id="dataset" class="column">
        <div id="row" class="dataset-field">
          <div id="subcolumn" class="dataset-title">
            <span>データカタログ</span>
          </div>
          <div id="subdataset" class="dataset-item">
            <a href="/dataset">
              <p class="dataset-item-num">
                {{ datasetCount }}
              </p>
              <p class="dataset-item-name">
                データセット
              </p>
            </a>
          </div>
          <div id="subclass" class="dataset-item">
            <a href="/organization">
              <p class="dataset-item-num">
                {{ organizationCount }}
              </p>
              <p class="dataset-item-name">
                組織
              </p>
            </a>
          </div>
          <div id="subgroup" class="dataset-item">
            <a href="/group">
              <p class="dataset-item-num">
                {{ groupCount }}
              </p>
              <p class="dataset-item-name">
                グループ
              </p>
            </a>
          </div>
          <div id="subtag" class="dataset-item">
            <a href="/tag">
              <p class="dataset-item-num">
                {{ tagCount }}
              </p>
              <p class="dataset-item-name">
                タグ
              </p>
            </a>
          </div>
        </div>
        <form method="get" action="/dataset" class="search_container">
          <input type="text" size="25" name="q" />
          <input type="submit" value="検索" />
        </form>
      </div>
      <a
        id="sandbox"
        href="https://hiroshima-sandbox.jp/"
        target="_blank"
        class="column inline-block"
      >
        <div class="sandbox-image" />
      </a>

      <a
        id="site-info"
        href="/about"
        class="column btn-square btn-large btn-square"
      >
        <img src="./assets/image/book.png" />本サイトについて
      </a>

      <a
        id="aboutuse"
        href="/about-use"
        class="column btn-square btn-large btn-square"
      >
        <img src="./assets/image/note.png" />ご利用について
      </a>

      <a id="opinion" href="/opinion" class="column btn-square btn-large">
        <img src="./assets/image/mail.png" />ご意見・ご要望
      </a>

      <div id="iotcanvas-button" class="column">
        <div class="title">
          IoT 連携
        </div>
        <div class="data btn-data">
          <a href="/organization/sandbox-lemon" class="btn-square btn-mini">島しょ部傾斜地<br />農業</a>
          <a href="/organization/sandbox-umi" class="btn-square btn-mini">海上交通</a>
          <a href="/organization/sandbox-seizou" class="btn-square btn-mini">ものづくり</a>
          <a href="/organization/sandbox-kaki" class="btn-square btn-mini">牡蠣養殖</a>
          <a href="/organization/sandbox-miyajima" class="btn-square btn-mini">宮島スマート観光</a>
          <!--
          <a
            href="https://hiroshima-sandbox.jp/#area4-project"
            target="_blank"
            class="btn-square btn-mini"
          >
            リアルタイム<br />データ連携事例
          </a>
          -->
        </div>
      </div>

      <div id="iotcanvas-map" class="column">
        <div class="title">
          可視化マップ
        </div>
      <a
        href="https://iotcanvas.cloud/619/sharing/maps?key=4cec06ed-10a2-4ed9-991f-71fba7f787b7"
        target="_blank"
        class="inline-block"
      >
        <div class="canvas iotcanvas-image">
          <!--<iframe
            src="https://iotcanvas.cloud/619/sharing/maps?key=4cec06ed-10a2-4ed9-991f-71fba7f787b7"
          />
          -->
        </div>
      </a>
        <div class="bottom-aria">
          <a
            href="https://iotcanvas.cloud/619/sharing/maps?key=4cec06ed-10a2-4ed9-991f-71fba7f787b7"
            target="_blank"
            class="button"
          >マップはこちら</a>
        </div>
      </div>

      <div id="iot-canvas" class="column">
        <div class="title">
          タグ別登録情報
        </div>
        <div class="canvas pieChart-center">
          <div class="canvas-margin" />
          <div class="canvas-grapharea">
            <div class="canvas-graph-labelarea">
              <div
                v-for="(label, index) in pieChart.labels"
                :key="index"
                class="canvas-graph-labels"
              >
                <div
                  class="canvas-graph-label-box"
                  :style="{
                    backgroundColor: pieChart.points.backgroundColor[index],
                  }"
                />
                <div>{{ label }}</div>
              </div>
            </div>
            <div class="canvas-graph-chartarea">
              <pie
                v-if="tagLoaded && showGraph"
                class="canvas-pieChart"
                :labels="pieChart.labels"
                :chartvalues="pieChart.points"
              />
            </div>
          </div>
          <div class="canvas-margin" />
        </div>
        <div class="bottom-aria">
          <a href="/tag" class="button">データカタログ</a>
        </div>
      </div>

      <div id="new-dataset" class="column">
        <div class="title">
          カタログ内データ（グラフ）
        </div>
        <line-chart
          v-if="tagLoaded"
          class="canvas-lineChart"
          :label="lineChartLabels"
          :chartvalues="lineChartPoints"
        />
        <line-chart
          v-if="tagLoaded"
          class="canvas-lineChart"
          :label="lineChartLabels2"
          :chartvalues="lineChartPoints2"
        />
        <div class="bottom-aria">
          <a
            href="https://iotcanvas.cloud/619/sharing/panels?key=ea8cf255-b692-4915-9cb5-c4a2ea04dff0"
            target="_blank"
            class="button"
          >他のデータはこちら</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import CkanApiRequest from '@/service/CkanApiRequest'
import FiwareApiRequest from '@/service/FiwareApiRequest'
import Pie from '@/components/graph/Pie.vue'
import LineChart from '@/components/graph/Line.vue'
import DatetimeService from '@/service/DatetimeService'
import GraphConst from '@/const/graphConst'
import { sleep } from '@/utils/Common'

import { PackageSearchResponse, PackageSearchResultTags } from './types/CkanApi'
import { FiwareResponse } from './types/FiwareApi'

type dataType = {
  showGraph: boolean
  resizeStatus: boolean
  datasetCount: number
  organizationCount: number
  groupCount: number
  tagCount: number
  lineChartLabels: string[]
  lineChartLabels2: string[]
  lineChartPoints: {
    label: string
    value: number[]
    yAxisID: string
    fill: boolean
    borderColor: string
    position: string
  }[]
  lineChartPoints2: {
    label: string
    value: number[]
    yAxisID: string
    fill: boolean
    borderColor: string
    position: string
  }[]
  pieChart: {
    labels: string[]
    points: {
      value: number[]
      backgroundColor: string[]
      fontAlign: string[]
      fontColor: string[]
    }
  }
  tagLoaded: boolean
  dataLoaded: boolean
}

const MAX_DISPLAY_PIE = 5
const UPPER_TAG_LENGTH = 5

export default Vue.extend({
  name: 'Home',
  components: {
    Pie,
    LineChart,
  },
  data(): dataType {
    return {
      showGraph: true,
      resizeStatus: false,
      datasetCount: 0,
      organizationCount: 0,
      groupCount: 0,
      tagCount: 0,
      lineChartLabels: [], // グラフラベル
      lineChartLabels2: [], // グラフラベル
      lineChartPoints: [], // グラフの点
      lineChartPoints2: [], // グラフの点
      tagLoaded: false,
      dataLoaded: false,
      pieChart: {
        labels: [],
        points: {
          value: [],
          backgroundColor: [],
          fontAlign: [],
          fontColor: [],
        },
      },
    }
  },
  async created() {
    const [
      datasetByOrganization,
      datasetByGroup,
      datasetByTag,
      graph1Left,
      graph1Right,
      graph2,
    ] = await Promise.all([
      CkanApiRequest.getDatasetByOrganization(),
      CkanApiRequest.getDatasetByGroup(),
      CkanApiRequest.getDatasetByTag(),
      FiwareApiRequest.getDatasetNumPerLine(
        GraphConst.COMET_ENTITY_TYPE,
        GraphConst.COMET_ENTITY_ID,
        GraphConst.GRAPH1_LEFT
      ),
      FiwareApiRequest.getDatasetNumPerLine(
        GraphConst.COMET_ENTITY_TYPE,
        GraphConst.COMET_ENTITY_ID,
        GraphConst.GRAPH1_RIGHT
      ),
      FiwareApiRequest.getDatasetNumPerLine(
        GraphConst.COMET_ENTITY_TYPE_2,
        GraphConst.COMET_ENTITY_ID_2,
        GraphConst.GRAPH2
      ),
    ])

    this.datasetCount = datasetByOrganization.count
    this.organizationCount = Object.keys(
      datasetByOrganization.facets.organization
    ).length
    this.groupCount = Object.keys(datasetByGroup.facets.groups).length
    this.tagCount = Object.keys(datasetByTag.facets.tags).length
    this.setTagList(datasetByTag)
    this.lineChartLabels = this.setLineChartLabels(graph1Left)
    this.lineChartLabels2 = this.setLineChartLabels(graph2)
    this.setLineChartPoints(
      graph1Left,
      this.lineChartPoints,
      GraphConst.GRAPH1_LEFT_NAME,
      GraphConst.YAXIS_1,
      GraphConst.GUIDE_1,
      GraphConst.LEFT
    )
    this.setLineChartPoints(
      graph1Right,
      this.lineChartPoints,
      GraphConst.GRAPH1_RIGHT_NAME,
      GraphConst.YAXIS_2,
      GraphConst.GUIDE_2,
      GraphConst.RIGHT
    )
    this.setLineChartPoints(
      graph2,
      this.lineChartPoints2,
      GraphConst.GRAPH2_NAME,
      GraphConst.YAXIS_1,
      GraphConst.GUIDE_3,
      GraphConst.LEFT
    )

    this.tagLoaded = true
    this.dataLoaded = true
  },
  methods: {
    // x軸の取得
    setLineChartLabels(response: FiwareResponse) {
      let returnLabel: string[] = []
      const points = this.checkFiwareResponse(response)
      returnLabel.splice(
        0,
        0,
        ...points.map((entity) => DatetimeService.getHour(entity.recvTime))
      )
      return returnLabel
    },
    // 座標点の取得
    setLineChartPoints(
      response: FiwareResponse,
      graphData: Array<Object>,
      label: string,
      axis: string,
      borderColor: string,
      position: string
    ) {
      let values: string[] = []
      const points = this.checkFiwareResponse(response)
      values.splice(0, 0, ...points.map((entity) => entity.attrValue))
      graphData.push({
        label: label,
        value: values,
        yAxisID: axis,
        fill: false,
        borderColor: borderColor,
        position: position,
      })
    },
    setPieChartLabels(labels: string[]) {
      this.pieChart.labels.splice(0, 0, ...labels)
    },
    setPieChartPoints(value: number[]) {
      this.pieChart.points = {
        value: value,
        backgroundColor: [
          '#41B677',
          '#41B88B',
          '#41BB9E',
          '#41BDB3',
          '#42B6BF',
          '#43A5C0',
        ],
        fontAlign: ['end', 'end', 'end', 'end', 'end', 'end'],
        fontColor: ['#000', '#000', '#000', '#000', '#000', '#000'],
      }
    },
    setTagList(response: PackageSearchResponse) {
      let data: number[] = []
      let labels: string[] = []
      let otherTags = 0

      const items = response.search_facets.tags.items
      items.sort((a, b) => ((a.count as number) > (b.count as number) ? -1 : 1))

      items.forEach((tag: PackageSearchResultTags, i) => {
        if (i >= MAX_DISPLAY_PIE) {
          otherTags += tag.count as number
          return
        }
        data.push(tag.count as number)
        labels.push(
          tag.name.length > UPPER_TAG_LENGTH
            ? `${tag.name.slice(0, UPPER_TAG_LENGTH)}..`
            : tag.name
        )
      })
      if (otherTags !== 0) {
        data.push(otherTags)
        labels.push('その他')
      }
      this.setPieChartLabels(labels)
      this.setPieChartPoints(data)
    },
    checkFiwareResponse(response: FiwareResponse) {
      const pointVal1 =
        response?.contextResponses[0]?.contextElement.attributes[0]?.values
      if (!pointVal1) {
        return []
      }

      return pointVal1
    },
    async handleResize() {
      if (this.resizeStatus) {
        return
      }

      this.resizeStatus = true
      await sleep(1000)

      this.showGraph = false
      await sleep(10)
      this.showGraph = true
      this.resizeStatus = false
    },
  },
  mounted: function () {
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy: function () {
    window.removeEventListener('resize', this.handleResize)
  },
})
</script>

<style lang="scss" scoped>
@import './assets/style/home.scss';
@import './assets/style/sublayout.scss';

@media only screen and (min-width: 768px) {
  @import './assets/style/pclayout.scss';
}
@media only screen and (max-width: 768px) {
  @import './assets/style/smartlayout.scss';
}
</style>
