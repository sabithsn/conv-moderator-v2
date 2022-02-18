<template>
  <div class="select" style="margin-top: 20px">
    <el-dropdown @command="handleCommand">
      <span class="el-dropdown-link" >
        Select batch<i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item v-for="batch in id_batches" :command="batch">{{batch}}</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<style>
  .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>

<script>
  export default {
    created() {
      this.token = sessionStorage.getItem('token')
      console.log(this.token)
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
      that.$axios.post("http://3.138.110.97:5000/index", data, config).then(function (response) {
          console.log(response.data);
          if(parseInt(response.data.code) === 400){
            that.$message('ERROR!')
          }else if (parseInt(response.data.code) === 200){
            that.id_batches = response.data.id_batches
            console.log(that.id_batches)
          }
        }).catch(function (error) {
          console.log(error)
        })
    },
    methods: {
      handleCommand(command) {
        console.log('click on batch ' + command)
        sessionStorage.setItem('id_batch', command)
        sessionStorage.setItem('id_image', 1)
        this.$router.push('caption')
      }
    },
    data: function() {
      return {
        id_batches: [
        ],
        selected_game: null
      }
    }
  }
</script>
