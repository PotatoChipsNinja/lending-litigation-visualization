<template>
  <v-container>
    <div class="text-h5 my-2">文书检索</div>
    <v-divider></v-divider>
    <v-row class="mt-2">
      <v-text-field
        v-model="keywords"
        outlined
        clearable
        label="请输入关键词进行检索"
        :error-messages="errMsg"
        @input="errMsg = ''"
        class="mx-4 my-2"
        dense
        append-icon="mdi-magnify"
        @click:append="search(0, 10)"
        @keydown="keyevent"
      >
      </v-text-field>
    </v-row>

    <v-row v-show="searched">
      <div class="ml-6">共找到 {{ cnt }} 条结果</div>
    </v-row>
    <v-row v-show="searched">
      <v-card
        v-for="(item, i) in items"
        :key="i"
        elevation="2"
        class="my-2 mx-4 pb-2"
        @click="dialog = true; dialogItem = item"
      >
        <v-card-title>{{ item.title }}</v-card-title>
        <v-card-subtitle>
          <v-row class="mx-1">
            {{ item.judge_date }} {{ item.caseNO }}
            <v-spacer></v-spacer>
            相关度：{{ item.tfidf.toFixed(4) }}
          </v-row>
        </v-card-subtitle>
        <v-card-text class="text--primary two-lines" style="height: 3rem;">
          {{ item.content }}
        </v-card-text>
      </v-card>
    </v-row>

    <v-row v-show="searched" class="d-flex justify-center mb-4">
      <v-pagination
        v-model="page"
        :length="Math.ceil(cnt/10)"
        :total-visible="8"
        @input="turn"
        v-show="searched"
      ></v-pagination>
    </v-row>

    <v-dialog
      v-model="dialog"
      width="60%"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ dialogItem.title }}</span>
        </v-card-title>
        <v-card-text>
          <v-row class="my-2">
            <v-chip
              class="ma-1"
              color="primary"
              small
              v-for="label in dialogItem.label.level1"
              :key="label"
            >
              {{ label }}
            </v-chip>
            <v-chip
              class="ma-1"
              color="primary lighten-1"
              small
              v-for="label in dialogItem.label.level2"
              :key="label"
            >
              {{ label }}
            </v-chip>
            <v-chip
              class="ma-1"
              color="primary lighten-2"
              small
              v-for="label in dialogItem.label.level3"
              :key="label"
            >
              {{ label }}
            </v-chip>
          </v-row>
          <v-row>
            {{ dialogItem.content }}
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            确定
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
  export default {
    name: 'Search',

    data: () => ({
      searched: false,
      keywords: '',
      errMsg: '',
      cnt: 0,
      items: [],
      dialog: false,
      dialogItem: {
        title: '',
        content: '',
        label: {
          level1: [],
          level2: [],
          level3: []
        }
      },
      page: 1
    }),

    methods: {
      search: function (start, end) {
        if (!this.keywords) {
          this.errMsg = '关键词不能为空'
        } else {
          this.searched = true
          this.$axios.get('/search_article', {
              params: {
                keywords: this.keywords,
                start: start,
                end: end
              }
            })
            .then((res) => {
              this.cnt = res.data.cnt
              this.items = res.data.items
            })
            .catch((err) => {
              console.log(err)
              this.$toast.error('与服务器连接出错')
            })
        }
      },
      turn: function (page) {
        this.search((page-1)*10, page*10)
      },
      keyevent: function (event) {
        if (event.key == 'Enter') {
          this.search(0, 10)
        }
      }
    }
  }
</script>
