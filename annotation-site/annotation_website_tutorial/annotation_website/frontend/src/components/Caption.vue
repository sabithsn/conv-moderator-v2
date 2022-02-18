<template>

  <!--<div class="caption">-->

  <div class="caption">
    <vue-grid align="stretch" justify="start">
      <vue-cell width="fill">
        <vue-topprogress ref="topProgress"></vue-topprogress>
        <el-row>
          <el-input type="number" min="1" max="99999999" v-model="jump_input" style="width: auto"
                    placeholder="The image you want to jump to"></el-input>
          <el-button v-on:click="jumpto" @change="keyhandler">Jump to</el-button>
          <el-button v-on:click="previous_pair" @change="keyhandler">Previous</el-button>
          <el-button v-on:click="next_pair" @change="keyhandler">Next</el-button>
        </el-row>
        <meta content="width=device-width,initial-scale=1" name="viewport"/>
        <section class="container" id="TaggingOfAnImage">
          <div class="row">
            <div class="col-xs-12 col-md-12"><!-- Instructions -->
              <div class="panel panel-primary">
                <!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature -->
                <el-link class="button" style="color: #66CCFF;" v-on:click="click_2_expand"><strong>Tagging Instructions
                  (Click to expand)</strong></el-link>
                <div class="panel-body" id="instructionBody"
                     :style="{display: expand_instruction === true ? 'block' : 'none'}">
                  <p> Select the statements that are true of the following image and caption.</p>
                  <p><u> You can select more than one option. </u></p>
                </div>

                &nbsp; &nbsp;&nbsp;
                <!--</p>-->
                <p>Image No. {{id_image}}</p>
                <!--<div style="display: block"> next image: {{next_image}}</div>-->

                <img style="
              max-height: 600px;
              max-width: 90%;
              height:auto;
              width:auto;" :src="url">

                <p><b>Caption:</b> {{text_caption}} </p>
              </div>
            </div>
          </div>

        </section>
      </vue-cell>
    </vue-grid>
    <vue-grid align="stretch" justify="start">
      <vue-cell width="3of12"/>
      <vue-cell width="6of12">
        <!-- End Instructions --><!-- Image Tagging Layout -->

        <b>Discourse relation</b>

        <div class="row" id="workContent">

          <el-row>
            <div class="cbBrokenImg" align="left">
              <el-checkbox v-model="cbBrokenImg"> The image is not showing up.</el-checkbox>
            </div>
          </el-row>

          <el-row>
            <div class="cb0" align="left">
              <el-checkbox v-model="cb0"><b>Meta:</b> The caption talks about when/where/how the picture is taken.
              </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbWhen" align="left" :style="{display: cb0 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbWhen">├─ When</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbHow" align="left" :style="{display: cb0 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbHow">├─ Where</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbWhere" align="left" :style="{display: cb0 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbWhere">└─ How</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbMetaGood" align="left" :style="{display: cb0 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbMetaGood">└─ Is the caption a good meta?</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbMetaBad" align="left" :style="{display: cb0 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbMetaBad">└─ Is the caption a bad meta?</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb1" align="left">
              <el-checkbox v-model="cb1"><b>Visible:</b> The caption is true just by looking at the picture.
              </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbVisible1" align="left" :style="{display: cb1=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbVisible1">└─ 1 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbVisible2" align="left" :style="{display: cb1=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbVisible2">└─ 2 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbVisible3" align="left" :style="{display: cb1=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbVisible3">└─ 3 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbVisible4" align="left" :style="{display: cb1=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbVisible4">└─ 4 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbVisible5" align="left" :style="{display: cb1=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbVisible5">└─ 5 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb2" align="left">
              <el-checkbox v-model="cb2"><b>Action:</b> The image describes an action</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb3" align="left">
              <el-checkbox v-model="cb3"><b>Subjective:</b> The caption is the matter of opinion.</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbSubjectiveGood" align="left" :style="{display: cb3 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbSubjectiveGood">└─ Is the caption a good subjective?</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbSubjectiveBad" align="left" :style="{display: cb3 === true ? 'block' : 'none'}">
              <el-checkbox v-model="cbSubjectiveBad">└─ Is the caption a bad subjective?</el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb4" align="left">
              <el-checkbox v-model="cb4"><b>Story:</b> Text and image work together like story and illustration.
              </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbStory1" align="left" :style="{display: cb4=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbStory1">└─ 1 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbStory2" align="left" :style="{display: cb4=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbStory2">└─ 2 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbStory3" align="left" :style="{display: cb4=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbStory3">└─ 3 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbStory4" align="left" :style="{display: cb4=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbStory4">└─ 4 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cbStory5" align="left" :style="{display: cb4=== true ? 'block' : 'none'}">
              <el-checkbox v-model="cbStory5">└─ 5 </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb5" align="left">
              <el-checkbox v-model="cb5"><b>Irrelevant:</b> Text does not seem to be written by a person in relation to
                this specific image.
              </el-checkbox>
            </div>
          </el-row>

          <el-row>
            <div class="Identification" align="left">
              <el-checkbox v-model="Identification"><b>Identification: </b>Text is identifying something in the image.
              </el-checkbox>
            </div>
          </el-row>
          <el-row>
            <div class="cb6" align="left">
              <el-checkbox v-model="cb6"><b>Other</b></el-checkbox>
            </div>
          </el-row>
          <el-input v-model="input" align="left" placeholder="You can write your other observations here." rows="5" type="textarea" :style="{display: cb6 === false ? 'none' : 'block'}"
                    :disabled="cb6 === false"></el-input>
        </div>
      </vue-cell>

      <vue-cell width="12of12">
        <el-row>
          <el-button v-on:click="submit">Submit discourse relation</el-button>
        </el-row>
      </vue-cell>
    </vue-grid>

  </div>

</template>

<style>
  div {
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .par-topic {
    color: dimgrey;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    line-height: 1;
    font-size: 11pt;
  }
</style>

<script>

  import {vueTopprogress} from 'vue-top-progress'
  import {VueCell, VueGrid} from 'vue-grd';

  export default {

    created() {
      this.update()
    },

    data() {
      return {
        expand_instruction: false,
        cbBrokenImg: false,
        cb0: false,
        cb1: false,
        cb2: false,
        cb3: false,
        cb4: false,
        cb5: false,
        cb6: false,
        Identification: false,
        cbWhen: false,
        cbHow: false,
        cbWhere: false,
        cbMetaGood: false,
        cbMetaBad: false,
        cbSubjectiveGood: false,
        cbSubjectiveBad: false,
        cbVisible1: false,
        cbVisible2: false,
        cbVisible3: false,
        cbVisible4: false,
        cbVisible5: false,
        cbStory1: false,
        cbStory2: false,
        cbStory3: false,
        cbStory4: false,
        cbStory5: false,
        input: '',
        cbPro: false,
        cbProRefText: false,
        cbProRefImg: false,
        jump_input: '',
        text_caption: '',
        id_image: 0,
      };
    },

    mounted() {

      this.$refs.topProgress.start();

      // Use setTimeout for demo
      let that = this;
      setTimeout(() => {
        that.$refs.topProgress.done()
      }, 2000)
    },

    components: {
      VueGrid,
      VueCell,
      vueTopprogress
    },

    methods: {
      clearinput: function () {
        this.expand_instruction = false;
        this.url = "";
        this.cbBrokenImg = false;
        this.cb0 = false;
        this.cb1 = false;
        this.cb2 = false;
        this.cb3 = false;
        this.cb4 = false;
        this.cb5 = false;
        this.cb6 = false;
        this.Identification = false;
        this.cbWhen = false;
        this.cbHow = false;
        this.cbWhere = false;
        this.cbMetaGood = false,
        this.cbMetaBad = false,
        this.cbSubjectiveGood = false,
        this.cbSubjectiveBad = false,
        this.cbVisible1 = false,
        this.cbVisible2 = false,
        this.cbVisible3 = false,
        this.cbVisible4 = false,
        this.cbVisible5 = false,
        this.cbStory1 = false,
        this.cbStory2 = false,
        this.cbStory3 = false,
        this.cbStory4 = false,
        this.cbStory5 = false,
        this.input = '';
        this.text_caption = '';
        this.source = 'None';
      },
      click_2_expand: function () {
        if (this.expand_instruction === true) {
          this.expand_instruction = false
        } else {
          this.expand_instruction = true
        }
      },
      update: function () {
        this.clearinput();
        this.token = sessionStorage.getItem('token');
        this.id_batch = sessionStorage.getItem('id_batch');
        this.id_image = sessionStorage.getItem('id_image');
        // this.next_image = sessionStorage.getItem('next_image');
        let that = this;
        let config = {
          headers: {
            "Content-Type": "application/json",
            "token": that.token,
            "id_batch": that.id_batch,
            "id_image": that.id_image,
          }
        };
        let data = {
          'HTTP_CONTENT_LANGUAGE': self.language
        };
        this.$axios.post("http://3.138.110.97:5000/getone", data, config).then(function (response) {
          console.log(response.data);
          if (parseInt(response.data.code) === 400) {
            that.msg('ERROR!')
          } else if (parseInt(response.data.code) === 200) {
            that.text_caption = response.data.caption;
            that.url = response.data.url;
            that.source = response.data.source;
            that.handleCurrentChange(1);
          }
        }).catch(function (error) {
          console.log(error)
        })
      },
      login: function () {
        console.log('pressed submit');
        console.log(this.id_annotator);
        let that = this;
        that.$axios.post('http://3.138.110.97:5000/login', {
          'id_annotator': that.id_annotator,
          'passwd_annotator': that.passwd_annotator
        }, {emulateJSON: true}).then(function (response) {
          console.log(response.data);
          if (parseInt(response.data.code) === 400) {
            that.id_annotator = '';
            that.passwd_annotator = '';
          } else if (parseInt(response.data.code) === 200) {
            sessionStorage.setItem('token', response.data.token);
            that.$router.push('index')
          }
        }).catch(function (error) {
          console.log(error)
        })
      },
      jumpto: function () {
        this.token = sessionStorage.getItem('token');
        this.id_batch = sessionStorage.getItem('id_batch');
        this.id_image = sessionStorage.getItem('id_image');
        // this.next_image = sessionStorage.getItem('next_image');
        let that = this;
        let config1 = {
          headers: {
            "Content-Type": "application/json",
            "token": that.token,
            "id_batch": that.id_batch,
            "id_image": that.jump_input,
          }
        };
        let data = {
          'HTTP_CONTENT_LANGUAGE': self.language
        };
        that.clearinput();
        that.$axios.post("http://3.138.110.97:5000/getone", data, config1).then(function (response) {
          console.log(response.data);
          if (parseInt(response.data.code) === 400) {
            that.msg(response.data.msg)
          } else if (parseInt(response.data.code) === 200) {
            that.clearinput();
            that.id_image = that.jump_input;
            that.text_caption = response.data.caption;
            that.url = response.data.url;
            that.source = response.data.source;
            that.handleCurrentChange(1);
          }
        }).catch(function (error) {
          console.log(error)
        })
      },
      previous_pair: function () {
        this.jump_input = parseInt(this.id_image) - 1
        this.jumpto()
      },
      next_pair: function () {
        this.jump_input = parseInt(this.id_image) + 1
        this.jumpto()
      },
      keyhandler: function (event) {
        console.log(event);

        if (event.key === "e") {
          this.$message('asd');
          event.key = "";
          event.preventDefault();
        }
      },
      msg: function (msg_text) {
        console.log(msg_text);
        this.$message({
          showClose: true,
          message: msg_text
        })
      },
      submit: function () {
        // Discourse relation
        let that = this;
        let cbBrokenImgv = this.cbBrokenImg ? "1" : "0";
        let cb0v = this.cb0 ? "1" : "0";
        let cb1v = this.cb1 ? "1" : "0";
        let cb2v = this.cb2 ? "1" : "0";
        let cb3v = this.cb3 ? "1" : "0";
        let cb4v = this.cb4 ? "1" : "0";
        let cb5v = this.cb5 ? "1" : "0";
        let cb6v = this.cb6 ? "1" : "0";
        let Identificationv = this.Identification ? "1" : "0";
        let cbWhenv = this.cb0 ? (this.cbWhen ? "1" : "0") : "0";
        let cbHowv = this.cb0 ? (this.cbHow ? "1" : "0") : "0";
        let cbWherev = this.cb0 ? (this.cbWhere ? "1" : "0") : "0";
        let cbMetaGoodv = this.cb0 ? (this.cbMetaGood ? "1" : "0") : "0";
        let cbMetaBadv = this.cb0 ? (this.cbMetaBad ? "1" : "0") : "0";
        let cbSubjectiveGoodv = this.cb3 ? (this.cbSubjectiveGood ? "1" : "0") : "0";
        let cbSubjectiveBadv = this.cb3 ? (this.cbSubjectiveBad ? "1" : "0") : "0";
        let cbVisible1v = this.cb1 ? (this.cbVisible1 ? "1" : "0") : "0";
        let cbVisible2v = this.cb1 ? (this.cbVisible2 ? "1" : "0") : "0";
        let cbVisible3v = this.cb1 ? (this.cbVisible3 ? "1" : "0") : "0";
        let cbVisible4v = this.cb1 ? (this.cbVisible4 ? "1" : "0") : "0";
        let cbVisible5v = this.cb1 ? (this.cbVisible5 ? "1" : "0") : "0";
        let cbStory1v = this.cb4 ? (this.cbStory1 ? "1" : "0") : "0";
        let cbStory2v = this.cb4 ? (this.cbStory2 ? "1" : "0") : "0";
        let cbStory3v = this.cb4 ? (this.cbStory3 ? "1" : "0") : "0";
        let cbStory4v = this.cb4 ? (this.cbStory4 ? "1" : "0") : "0";
        let cbStory5v = this.cb4 ? (this.cbStory5 ? "1" : "0") : "0";

        let text_other = this.cb6 ? this.input : "";
        let source = this.source;
        console.log(cb0v, cb1v, cb3v, cb4v, cb5v, Identificationv, cb6v, cbWhenv, cbHowv, cbWherev, cbMetaGoodv, cbMetaBadv, cbSubjectiveGoodv, cbSubjectiveBadv, cbVisible1v, cbVisible2v, cbVisible3v, cbVisible4v, cbVisible5v, cbStory1v, cbStory2v, cbStory3v, cbStory4v,cbStory5v, text_other);
        console.log(source);

        if (this.cb0 === true) {
          if (this.cbWhen === false && this.cbHow === false && this.cbWhere == false && this.cbMetaGood == false && this.cbMetaBad == false) {
            this.$alert('You have to select at least one of "When/Where/How/Good/Bad" if you selected "The caption talks about when and how the picture is taken."');
            return;
          }
        }

        if (this.cb1 === true) {
          if (this.cbVisible1 === false && this.cbVisible2 === false && this.cbVisible3 == false && this.cbVisible4 == false && this.cbVisible5 == false) {
            this.$alert('You have to select at least one rating for Visible!');
            return;
          }
        }

        if (this.cb3 === true) {
          if (this.cbSubjectiveBad === false && this.cbSubjectiveGood === false) {
            this.$alert('You have to select at least one rating for Subjective!');
            return;
          }
        }

        if (this.cb4 === true) {
          if (this.cbStory1 === false && this.cbStory2 === false && this.cbStory3 == false && this.cbStory4 == false && this.cbStory5 == false) {
            this.$alert('You have to select at least one rating for Story!');
            return;
          }
        }

        let config = {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "token": that.token,
            "id_batch": that.id_batch,
            "id_image": that.id_image,
            "url": that.url,
            "caption": that.text_caption,
          }
        };
        let data = {
          'HTTP_CONTENT_LANGUAGE': self.language,
          'cbBrokenImg': cbBrokenImgv,
          'cb0': cb0v,
          'cb1': cb1v,
          'cb2': cb2v,
          'cb3': cb3v,
          'cb4': cb4v,
          'cb5': cb5v,
          'cb6': cb6v,
          'Identification': Identificationv,
          'cbWhen': cbWhenv,
          'cbHow': cbHowv,
          'cbWhere': cbWherev,
          'cbMetaGood': cbMetaGoodv,
          'cbMetaBad': cbMetaBadv,
          'cbSubjectiveGood': cbSubjectiveGoodv,
          'cbSubjectiveBad': cbSubjectiveBadv,
          'cbVisible1': cbVisible1v,
          'cbVisible2': cbVisible2v,
          'cbVisible3': cbVisible3v,
          'cbVisible4': cbVisible4v,
          'cbVisible5': cbVisible5v,
          'cbStory1': cbStory1v,
          'cbStory2': cbStory2v,
          'cbStory3': cbStory3v,
          'cbStory4': cbStory4v,
          'cbStory5': cbStory5v,
          'other': text_other,
          'source': source
        };
        that.$axios.post("http://3.138.110.97:5000/annotate", data, config).then(function (response) {
          console.log(config);
          console.log(data);
          console.log(response.data);
          if (parseInt(response.data.code) === 400) {
            that.msg('ERROR!')
          } else if (parseInt(response.data.code) === 200) {
            // that.id_image = response.data.id_image
            let msg_text = 'Discourse relation for image ' + that.id_image + ' saved.';
            that.msg(msg_text);
            that.next_image = response.data.id_image;
            if (that.next_image === -1) {
              that.msg('You have finished batch ' + that.id_batch)
              that.$router.push('select')
            } else {
              sessionStorage.setItem('id_image', that.next_image)
              that.update()
              // pass
            }
          }
        }).catch(function (error) {
          console.log(error)
        });
      }
    }
  }

</script>
