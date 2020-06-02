<script>
// ここでこのコンポーネントで使用するグラフの種類を定義する。今回は円グラフなのでPieとなる。
import { Pie } from 'vue-chartjs'
import ChartJsPluginDataLabels from 'chartjs-plugin-datalabels'

export default {
  components: {
    ChartJsPluginDataLabels,
  },
  extends: Pie,
  props: {
    labels: {
      type: Array,
      required: true,
    },
    chartvalues: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      data: {
        labels: this.labels,
        //データセット
        datasets: [
          {
            //背景色
            backgroundColor: this.chartvalues.backgroundColor,
            //グラフのデータ
            data: this.chartvalues.value,
          },
        ],
      },
      options: {
        legend: {
          display: false,
          labels: {
            boxWidth: 20,
            fontSize: 14,
            fontColor: '#000000',
            padding: 15,
          },
        },
        plugins: {
          datalabels: {
            formatter: function (datasets) {
              return datasets + '件'
            },
            align: this.chartvalues.fontAlign,
            font: {
              size: 14,
              weight: 'bold',
            },
            color: this.chartvalues.fontColor,
          },
        },
      },
    }
  },
  mounted() {
    this.renderChart(this.data, this.options)
  },
}
</script>
