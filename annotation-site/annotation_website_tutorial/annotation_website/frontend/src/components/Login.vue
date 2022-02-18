<template>
  <div id="app">
    <form novalidate>
      <label for="id_annotator" style="margin-left: 54px">ID:</label>
      <el-input type="text" placeholder="Please enter your ID" id="id_annotator" v-model="id_annotator" style="width: auto"/>
      <br>
      <label for="passwd_annotator">Password:</label>
      <el-input type="password" placeholder="Please enter your password" id="passwd_annotator" v-model="passwd_annotator" style="width: auto"/>
      <br>
      <el-button v-on:click="login" type="button">Login</el-button>
    </form>
  </div>
</template>

<script>
  /*js*/
  export default {
    name: 'login',
    data: function () {
      return {
        id_annotator: '',
        passwd_annotator: ''
      }
    },
    methods: {
      login: function () {
        console.log('pressed login')
        console.log(this.id_annotator)
        let that = this;
        that.$axios.post('http://3.138.110.97:5000/login', {
          'id_annotator': that.id_annotator,
          'passwd_annotator': that.passwd_annotator
        }, {emulateJSON: true}).then(function (response) {
          console.log(response.data);
          if(parseInt(response.data.code) === 400){
            that.id_annotator = '';
            that.passwd_annotator = '';
          }else if (parseInt(response.data.code) === 200){
            that.token = response.data.token
            sessionStorage.setItem('token', that.token);
            if (that.token === 'admin') {
              that.$router.push('admin')
            }
            else {
              that.$router.push('select')
            }
          }
        }).catch(function (error) {
          console.log(error)
        })
      }
    }
  }
</script>
