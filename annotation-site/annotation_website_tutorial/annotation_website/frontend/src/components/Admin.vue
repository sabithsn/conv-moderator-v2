<template>
  <div id="app">
      <el-button v-on:click="totsv" type="button">Export to tsv</el-button>
      <el-button v-on:click="rmdb" type="button">Delete database</el-button>
      <el-input v-model="input" type="text" v-bind:style="{width: 'auto', visibility: vis}" placeholder="Input CONFIRM here" ></el-input>
  </div>
</template>

<script>
  /*js*/
  export default {
    name: 'admin',
    created () {
      this.token = sessionStorage.getItem('token')
        if (this.token !== 'admin') {
            this.$router.push('login')
        }
    },
    data: function () {
      return {
        id_annotator: '',
        passwd_annotator: '',
        vis: 'hidden',
        input: ''
      }
    },
    methods: {
      totsv: function () {
        let that = this
        let config = {
          headers: {
                "Content-Type": "application/json",
                "token": that.token,
            }
          }
          let data = {
            'HTTP_CONTENT_LANGUAGE': self.language
          }
          that.$axios.post("http://3.138.110.97:5000/export", data, config).then(function (response) {
              console.log(response.data);
              if(parseInt(response.data.code) === 400){
                that.$message('ERROR!')
              }else if (parseInt(response.data.code) === 200){
                that.download()
              }
            }).catch(function (error) {
              console.log(error)
            })
      },
      download: function() {
        console.log('Trying to download')
        let that = this
        that.$axios.get("http://3.138.110.97:5000/download", {headers: {"token": that.token}}).then(response => {
            console.log(response)
            let url = window.URL.createObjectURL(new Blob([response.data]))
            let link = document.createElement('a')
            link.href = url
            link.setAttribute('download', 'output.tsv')
            document.body.appendChild(link)
            link.click()
          }).catch(() => console.log('error'))
      },
      rmdb: function () {
        if (this.vis === 'hidden') {
            this.$message('Please input `CONFIRM`')
            this.vis = 'visible'
        }
        else if(this.input !== 'CONFIRM') {
            this.$message('Please input `CONFIRM`')
            this.input = ''
        }
        else {
            let that = this
            that.$axios.get("http://3.138.110.97:5000/rmdb", {headers: {"token": that.token}}).then(response => {
                console.log(response)
                if (response.data.code === 200) {
                    that.$message('Deletion completed.')
                }
                else {
                    that.$message('Some error occurred.')
                }}).catch(() => console.log('error'))
        }

      }
    }
  }
</script>
