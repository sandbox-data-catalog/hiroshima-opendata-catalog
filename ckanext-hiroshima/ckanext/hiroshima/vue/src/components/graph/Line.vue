<script>
// ここでこのコンポーネントで使用するグラフの種類を定義する。今回は線形グラフなのでLineとなる。
import { Line, mixins } from 'vue-chartjs'
import ChartJsPluginDataLabels from 'chartjs-plugin-datalabels'
const { reactiveProp } = mixins

export default {
  components: {
    ChartJsPluginDataLabels,
  },
  extends: Line,
  mixins: [reactiveProp],
  props: {
    label: {
      type: Array,
      required: true,
    },
    chartvalues: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      data: {
        //データ項目のラベル
        labels: this.label,
        //データセット
        datasets: this.chartvalues.map((chart) => {
          return {
            label: chart.label,
            //グラフのデータ
            data: chart.value,
            yAxisID: chart.yAxisID,
            fill: chart.fill,
            borderColor: chart.borderColor,
          }
        }),
      },
      options: {
        maintainAspectRatio: false,
        legend: {
          display: true,
          labels: {
            boxWidth: 30,
            fontSize: 14,
            fontColor: 'black',
            padding: 10,
          },
        },
        plugins: {
          datalabels: {
            display: 'auto',
          },
        },
        scales: {
          xAxes: [
            {
              ticks: {
                fontColor: 'black',
                fontSize: 14,
              },
            },
          ],
          yAxes: this.chartvalues.map((chart) => {
            return {
              id: chart.yAxisID, // set unique name of axis on the left
              position: chart.position,
              scaleLabel: {
                display: true,
                labelString: chart.label,
                fontColor: chart.borderColor,
              },
              ticks: {
                fontColor: 'black',
                fontSize: 14,
              },
              gridLines: {
                zeroLineColor: 'black',
              },
            }
          }),
        },
      },
    }
  },
  mounted() {
    this.renderChart(this.data, this.options)
  },
}
</script>
