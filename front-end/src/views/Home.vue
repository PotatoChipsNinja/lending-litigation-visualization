<template>
  <v-container class="pa-8">
    <v-row class="my-4">
      <v-col cols="12" class="d-flex justify-center">
        <v-img
          :src="require('../assets/thu_logo.svg')"
          max-width="100"
          max-height="100"
        />
        <v-divider vertical class="ml-6 mr-4"></v-divider>
        <v-img
          :src="require('../assets/thu_law_logo.svg')"
          max-width="100"
          max-height="100"
        />
      </v-col>

      <v-col cols="12" class="d-flex justify-center">
        <div class="text-h4 font-weight-light">{{ username }}, 欢迎使用民间借贷诉讼数据可视化系统</div>
      </v-col>

      <v-col cols="12" class="d-flex justify-center pt-0">
        <div class="text--secondary font-weight-light">通过下方卡片快捷进入功能页，或通过侧边栏进行导航</div>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col
        v-for="(item, i) in items"
        :key="i"
        cols="6"
      >
        <v-card
          :color="!$vuetify.theme.dark ? item.color : ''"
          dark
        >
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title
                class="text-h5"
                v-text="item.title"
              ></v-card-title>

              <v-card-subtitle style="height: 2rem;" v-text="item.description"></v-card-subtitle>

              <v-card-actions>
                <v-btn
                  class="ml-2 mt-5"
                  outlined
                  rounded
                  small
                  :to="item.route"
                >
                  立即查看
                </v-btn>
              </v-card-actions>
            </div>

            <v-avatar
              class="ma-3"
              size="125"
              tile
            >
              <v-icon size="80" v-text="item.icon"></v-icon>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Home',

    props: {
      username: String
    },

    data: () => ({
      items: [
        {
          color: '#1F7087',
          title: '文书检索',
          description: '根据任意关键词、案件名称、法院统一案件编号、案情标签等信息对文书进行检索...',
          icon: 'mdi-text-box-search',
          route: '/search'
        },
        {
          color: '#952175',
          title: '当事人分析',
          description: '分析特定案情下原告或被告的年龄结构、性别分布...',
          icon: 'mdi-account-multiple',
          route: '/party'
        },
        {
          color: '#26c6da',
          title: '案情标签分析',
          description: '分析三级案情标签的分布情况...',
          icon: 'mdi-label-multiple',
          route: '/label'
        },
        {
          color: '#9e9d24',
          title: '判决机构分布',
          description: '分析特定案情下的法院分布、所属行政区划分布等信息...',
          icon: 'mdi-office-building-marker',
          route: '/court'
        },
        {
          color: '#7986CB',
          title: '判决时间分布',
          description: '分析特定案情下的案件数量随时间变化趋势...',
          icon: 'mdi-calendar-clock',
          route: '/time'
        },
        {
          color: '#00897B',
          title: '判决结果分布',
          description: '分析特定案情下的判决结果分布情况...',
          icon: 'mdi-gavel',
          route: '/decision'
        },
        {
          color: '#7CB342',
          title: '引用法律分布',
          description: '分析特定案情下的法律引用分布情况...',
          icon: 'mdi-bookshelf',
          route: '/law'
        },
        {
          color: '#8D6E63',
          title: '引用条文分布',
          description: '分析特定案情、特定法律的法律条文引用分布情况...',
          icon: 'mdi-script-text',
          route: '/clause'
        }
      ]
    })
  }
</script>
