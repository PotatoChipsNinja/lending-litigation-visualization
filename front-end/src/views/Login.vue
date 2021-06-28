<template>
  <div class="d-flex justify-center" style="height: 100%">
    <v-col cols="6" align-self="center">
      <v-card class="overflow-hidden" color="login lighten-1" dark>
        <v-toolbar flat color="login">
          <v-icon>mdi-login-variant</v-icon>
          <v-toolbar-title class="font-weight-light ml-2">
            管理员登录
          </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-text-field
            tabindex="1"
            v-model="inputUsername"
            color="white"
            prepend-icon="mdi-account"
            label="用户名"
            :error-messages="usernameErrMsg"
            @input="usernameErrMsg = passwordErrMsg = ''"
            clearable
          ></v-text-field>
          <v-text-field
            tabindex="2"
            v-model="inputPassword"
            color="white"
            prepend-icon="mdi-form-textbox-password"
            label="密码"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show ? 'text' : 'password'"
            @click:append="show = !show"
            :error-messages="passwordErrMsg"
            @input="usernameErrMsg = passwordErrMsg = ''"
            clearable
          ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn tabindex="3" color="loginBtn" @click="login">
            登录
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </div>
</template>

<script>
  export default {
    name: 'Login',

    data: () => ({
      show: false,
      inputUsername: '',
      inputPassword: '',
      usernameErrMsg: '',
      passwordErrMsg: ''
    }),

    methods: {
      login: function () {
        if (!this.inputUsername) {
          this.usernameErrMsg = '用户名不能为空'
        } else if (!this.inputPassword) {
          this.passwordErrMsg = '密码不能为空'
        } else {
          let data = new FormData()
          data.append('username', this.inputUsername)
          data.append('password', this.inputPassword)

          this.$axios.post('/auth/login', data)
            .then(() => {
              localStorage.setItem('username', 'admin')
              this.$emit('update:username', 'admin')
              this.$toast.success('登录成功')
              this.$router.replace('/')
            })
            .catch((err) => {
              if (err.response && err.response.status == 403) {
                this.usernameErrMsg = this.passwordErrMsg = '用户名或密码错误'
              } else {
                console.log(err)
                this.$toast.error('与服务器连接出错')
              }
            })
        }
      }
    }
  }
</script>
