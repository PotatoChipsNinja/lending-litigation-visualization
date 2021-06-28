<template>
  <v-container>
    <div class="text-h5 my-2">判决机构分布</div>
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

    <div ref="chart3" style="height: 50rem;"></div>
    <div ref="chart2" style="height: 30rem;"></div>
    <div ref="chart1" style="height: 30rem;"></div>

  </v-container>
</template>

<script>
  export default {
    name: 'Court',

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
      },

      provinceData: function () {
        let ans = []
        for (let key in this.result.province) {
          ans.push({ name: key, value: this.result.province[key] })
        }
        return ans
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
          return b.value - a.value
        })

        for (let i = 0; i < temp.length && i < 10; i++) {
          ret.name.push(temp[i].name)
          ret.value.push(temp[i].value)
        }

        return ret
      },

      apply: function () {
        this.loading = true
        this.result = []

        this.$axios.get('/get_court_stat', {
            params: {
              labels: this.allLabel
            }
          })
          .then((res) => {
            this.result = res.data
            this.draw1()
            this.draw2()
            this.draw3()
          })
          .catch((err) => {
            console.log(err)
            this.$toast.error('与服务器连接出错')
          })
          .then(() => {
            this.loading = false
          })
      },
      draw1: function () {
        let myChart = this.$echarts.init(this.$refs.chart1)
        let option = {
          title: {
            text: '判决机构分布',
            subtext: '仅展示前十名',
            left: 'center'
          },
          toolbox: {
            show: true,
            feature: {
              saveAsImage: {show: true}
            }
          },
          yAxis: {
            type: 'category',
            data: this.sorted(this.result.court_name).name.reverse()
          },
          xAxis: {
            type: 'value'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          series: [{
            data: this.sorted(this.result.court_name).value.reverse(),
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            },
            label: {
              show: true,
              position: 'right',
              valueAnimation: true
            }
          }]
        }
        myChart.setOption(option)
      },
      draw2: function () {
        let myChart = this.$echarts.init(this.$refs.chart2)
        let option = {
          title: {
            text: '判决机构所在地分布',
            subtext: '仅展示前十名',
            left: 'center'
          },
          toolbox: {
            show: true,
            feature: {
              saveAsImage: {show: true}
            }
          },
          xAxis: {
            type: 'category',
            data: this.sorted(this.result.court_location).name
          },
          yAxis: {
            type: 'value'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          series: [{
            data: this.sorted(this.result.court_location).value,
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            },
            label: {
              show: true,
              position: 'top',
              valueAnimation: true
            }
          }]
        }
        myChart.setOption(option)
      },
      draw3: function () {
        let myChart = this.$echarts.init(this.$refs.chart3)
        this.$axios.get('/assets/china.json')
          .then((res) => {
            this.$echarts.registerMap('CN', res.data)
            let option = {
              title: {
                text: '判决机构所在省份分布',
                left: 'center'
              },
              toolbox: {
                show: true,
                feature: {
                  saveAsImage: {show: true}
                }
              },
              tooltip: {
                trigger: 'item',
                formatter: '{b}<br/>{c}'
              },
              visualMap: {
                min: 0,
                max: 1200,
                text: ['High', 'Low'],
                realtime: false,
                calculable: true,
                inRange: {
                    color: ['lightskyblue', 'yellow', 'orangered']
                },
                top: 'center'
              },
              series: [
                {
                  type: 'map',
                  mapType: 'CN',
                  label: {
                    show: true
                  },
                  data: this.provinceData
                }
              ]
            }
            myChart.setOption(option)
          })
          .catch((err) => {
            console.log(err)
            this.$toast.error('与服务器连接出错')
          })
      }
    }
  }
</script>
