<template>
  <v-container>
    <div class="text-h5 my-2">案情标签分析</div>
    <v-divider></v-divider>
    <v-row class="mt-2">
      <v-col style="max-width: 34rem">
        <v-card>
          <v-card-text class="px-8">
            <v-row align="center">
              <v-col cols="3" class="py-0">
                <v-subheader>
                  标签级别
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-radio-group v-model="level" row>
                  <v-radio
                    v-for="n in 3"
                    :key="n-1"
                    :label="strType[n-1]"
                    :value="n-1"
                  ></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text color="success" :loading="loading" @click="apply">
              查询
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <div ref="chart" style="height: 30rem;"></div>

    <v-row v-show="tableItems.length > 0">
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="tableItems"
          class="elevation-2"
          :loading="loadingTable"
          loading-text="加载中，请稍候"
          no-data-text="无可用数据"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Label',

    data: () => ({
      strType: ['第一级', '第二级', '第三级'],
      loading: false,
      level: 0,
      headers: [
        { text: '标签名称', value: 'label', align: 'center', class: 'pl-4 pr-0' },
        { text: '案件数量', value: 'cnt', align: 'center', class: 'pl-4 pr-0' }
      ],
      loadingTable: false,
      result: {}
    }),

    computed: {
      tableItems: function () {
        let ret = []
        for (let key in this.result) {
          ret.push({ label: key, cnt: this.result[key] })
        }
        ret.sort((a, b) => {
          return b.cnt - a.cnt
        })
        return ret
      },

      chartData: function () {
        let ret = []
        let table = this.tableItems
        for (let i = 0; i < table.length && i < 20; i++) {
          ret.push({ name: table[i].label, value: table[i].cnt })
        }
        let other = 0
        for (let i = 20; i < table.length; i++) {
          other += table[i].cnt
        }
        if (other > 0) {
          ret.push({ name: '其他', value: other })
        }
        return ret
      }
    },

    methods: {
      apply: function () {
        this.loading = true
        this.loadingTable = true
        this.result = []

        this.$axios.get('/get_label_stat', {
            params: {
              level: this.level
            }
          })
          .then((res) => {
            this.result = res.data
            this.draw()
          })
          .catch((err) => {
            console.log(err)
            this.$toast.error('与服务器连接出错')
          })
          .then(() => {
            this.loading = false
            this.loadingTable = false
          })
      },
      draw: function () {
        let myChart = this.$echarts.init(this.$refs.chart)
        let option = {
          legend: {
            show: false
          },
          toolbox: {
            show: true,
            feature: {
              saveAsImage: {show: true}
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: '{b} : {c} ({d}%)'
          },
          series: [
            {
              type: 'pie',
              radius: ['40%', '70%'],
              itemStyle: {
                borderRadius: 8
              },
              data: this.chartData
            }
          ]
        }
        myChart.setOption(option)
      }
    }
  }
</script>
