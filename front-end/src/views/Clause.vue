<template>
  <v-container>
    <div class="text-h5 my-2">引用条文分布</div>
    <v-divider></v-divider>
    <v-row class="my-2">
      <v-col style="max-width: 34rem">
        <v-card>
          <v-card-title>
            筛选
          </v-card-title>

          <v-divider></v-divider>
          <v-card-text class="px-8">
            <v-row align="center">
              <v-col cols="3" class="py-0">
                <v-subheader>
                  法律名称
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-select
                  v-model="law"
                  :items="lawList"
                  placeholder="未选择"
                ></v-select>
              </v-col>

              <v-col cols="3" class="py-0">
                <v-subheader>
                  一级标签
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-select
                  v-model="level1"
                  :items="labelList.level1"
                  placeholder="不筛选"
                  multiple
                  chips
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="3" class="py-0">
                <v-subheader>
                  二级标签
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-select
                  v-model="level2"
                  :items="labelList.level2"
                  placeholder="不筛选"
                  multiple
                  chips
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="3" class="py-0">
                <v-subheader>
                  三级标签
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-select
                  v-model="level3"
                  :items="labelList.level3"
                  placeholder="不筛选"
                  multiple
                  chips
                  clearable
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text color="success" :disabled="law == ''" :loading="loading" @click="apply">
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
          no-data-text="无可用数据"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Clause',

    data: () => ({
      law: '',
      lawList: ['dwq', '32'],
      level1: [],
      level2: [],
      level3: [],
      labelList: {
        level1: [],
        level2: [],
        level3: []
      },
      loading: false,
      result: {},
      headers: [
        { text: '条款', value: 'name', align: 'center', class: 'pl-4 pr-0' },
        { text: '条款内容', value: 'content', align: 'center', class: 'pl-4 pr-0', width: '75%' },
        { text: '引用次数', value: 'value', align: 'center', class: 'pl-4 pr-0' }
      ],
    }),

    computed: {
      allLabel: function () {
        let ans = [...this.level1, ...this.level2, ...this.level3]
        return ans.join(',')
      },

      tableItems: function () {
        let ret = []
        for (let key in this.result) {
          ret.push({ name: key, value: this.result[key].cnt, content: this.result[key].content })
        }
        ret.sort((a, b) => {
          return b.value - a.value
        })
        return ret
      },

      chartData: function () {
        let ret = []
        let table = this.tableItems
        for (let i = 0; i < table.length && i < 5; i++) {
          ret.push(table[i])
        }
        let other = 0
        for (let i = 5; i < table.length; i++) {
          other += table[i].value
        }
        if (other > 0) {
          ret.push({ name: '其他', value: other })
        }
        return ret
      }
    },

    mounted: function () {
      this.getLawList()
      this.getLabel(0)
      this.getLabel(1)
      this.getLabel(2)
    },

    methods: {
      getLabel: function (level) {
        this.$axios.get('/get_label', {
            params: {
              level: level
            }
          })
          .then((res) => {
            this.labelList['level' + (level+1).toString()] = res.data
          })
          .catch((err) => {
            console.log(err)
            this.$toast.error('与服务器连接出错')
          })
      },

      getLawList: function () {
        this.$axios.get('/get_law_stat')
          .then((res) => {
            let t = res.data
            let l = []
            for (let key in t) {
              l.push({ name: key, value: t[key] })
            }
            l.sort((a, b) => {
              return b.value - a.value
            })
            this.lawList = []
            for (let i = 0; i < l.length; i++) {
              this.lawList.push(l[i].name)
            }
          })
          .catch((err) => {
            console.log(err)
            this.$toast.error('与服务器连接出错')
          })
      },

      apply: function () {
        this.loading = true
        this.result = []

        this.$axios.get('/get_clause_stat', {
            params: {
              labels: this.allLabel,
              law: this.law
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
