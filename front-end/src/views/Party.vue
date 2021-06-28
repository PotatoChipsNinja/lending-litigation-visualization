<template>
  <v-container>
    <div class="text-h5 my-2">当事人分析</div>
    <v-divider></v-divider>
    <v-row class="my-2">
      <v-col style="max-width: 38rem">
        <v-card>
          <v-card-title>
            筛选
          </v-card-title>

          <v-divider></v-divider>
          <v-card-text class="px-8">
            <v-row align="center">
              <v-col cols="3" class="py-0">
                <v-subheader>
                  当事人角色
                </v-subheader>
              </v-col>
              <v-col cols="9" class="py-0">
                <v-radio-group v-model="role" row>
                  <v-radio
                    v-for="n in 2"
                    :key="n-1"
                    :label="n == 1 ? '原告' : '被告'"
                    :value="n-1"
                  ></v-radio>
                </v-radio-group>
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
            <v-btn text color="success" :loading="loading" @click="apply">
              查询
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="6">
        <div ref="chart1" style="height: 30rem;"></div>
      </v-col>
      <v-col cols="6">
        <div ref="chart2" style="height: 30rem;"></div>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
  export default {
    name: 'Party',

    data: () => ({
      role: 0,
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

      apply: function () {
        this.loading = true
        this.result = []

        this.$axios.get('/get_person_stat', {
            params: {
              labels: this.allLabel,
              defendant: this.role ? true : false
            }
          })
          .then((res) => {
            this.result = res.data
            this.draw1()
            this.draw2()
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
            text: '当事人性别分布',
            left: 'center'
          },
          legend: {
            top: '5%',
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
            formatter: '{b} : {c} ({d}%)'
          },
          series: [
            {
              type: 'pie',
              radius: ['40%', '70%'],
              itemStyle: {
                borderRadius: 8
              },
              data: [
                {value: this.result.gender.male, name: '男性'},
                {value: this.result.gender.female, name: '女性'}
              ]
            }
          ]
        }
        myChart.setOption(option)
      },
      draw2: function () {
        let myChart = this.$echarts.init(this.$refs.chart2)
        let option = {
          title: {
            text: '当事人年龄分布',
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
            data: ['18 岁以下', '18-25 岁', '25-40 岁', '40-55 岁', '55-70 岁', '70 岁以上']
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
            data: [
              this.result.age['小于18'],
              this.result.age['18-25'],
              this.result.age['25-40'],
              this.result.age['40-55'],
              this.result.age['55-70'],
              this.result.age['大于70']
            ],
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
      }
    }
  }
</script>
