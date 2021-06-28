<template>
  <v-container>
    <div class="text-h5 my-2">判决时间分布</div>
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
            <v-btn text color="success" :loading="loading" @click="apply">
              查询
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <div ref="chart" style="height: 30rem;"></div>

  </v-container>
</template>

<script>
  export default {
    name: 'Time',

    data: () => ({
      level1: [],
      level2: [],
      level3: [],
      labelList: {
        level1: [],
        level2: [],
        level3: []
      },
      loading: false,
      result: {}
    }),

    computed: {
      allLabel: function () {
        let ans = [...this.level1, ...this.level2, ...this.level3]
        return ans.join(',')
      }
    },

    mounted: function () {
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

      sorted: function (obj) {
        let ret = {
          name: [],
          value: []
        }

        let temp = []
        for (let key in obj) {
          temp.push({ name: key, value: obj[key] })
        }
        temp.sort((a, b) => {
          return parseInt(a.key) - parseInt(b.key)
        })

        for (let i = 0; i < temp.length; i++) {
          ret.name.push(temp[i].name)
          ret.value.push(temp[i].value)
        }

        return ret
      },

      apply: function () {
        this.loading = true
        this.result = []

        this.$axios.get('/get_year_stat', {
            params: {
              labels: this.allLabel
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
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: this.sorted(this.result).name
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: this.sorted(this.result).value,
            type: 'line',
            areaStyle: {},
            label: {
              show: true,
              position: 'top'
            },
            smooth: true
          }],
          toolbox: {
            show: true,
            feature: {
              saveAsImage: {show: true}
            }
          }
        }
        myChart.setOption(option)
      }
    }
  }
</script>
