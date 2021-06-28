import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
      themes: {
        light: {
          bar: '#3f51b5',
          login: '#00695c',
          loginBtn: '#00594c'
        },
        dark: {
          bar: '#37474f',
          login: '#263238',
          loginBtn: '#546e7a'
        }
      }
    }
});
