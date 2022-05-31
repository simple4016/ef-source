<template>
  <div class="box">
    <h1 class="low-title">
      <el-divider direction="vertical"></el-divider> Low Risk
    </h1>
    <low-risk v-if="!IsPhone && !isLow" />
    <low-risk-h5 v-if="IsPhone && !isLow" />
    <div class="divider" v-if="!isHigh"></div>
    <h1 class="high-title" v-if="!isHigh">
      <el-divider direction="vertical"></el-divider> High Risk

      <el-tooltip class="item" effect="dark" placement="top">
        <div slot="content">
          Note: High Risk strategies might have
          <br />higher possibility to lose principle in
          <br />
          compare to Low Risk strategies.
        </div>
        <i class="el-icon-question"></i>
      </el-tooltip>
    </h1>
    <high-risk v-if="!IsPhone && !isHigh" />
    <high-risk-h5 v-if="IsPhone && !isHigh" />
  </div>
</template>
<script>
import { mapState } from 'vuex'
import { HMarkets, LMarkets } from '../../config.js'
export default {
  name: 'Cff',
  components: {
    LowRisk: () => import('./LowRisk.vue'),
    LowRiskH5: () => import('./LowRiskH5.vue'),
    HighRisk: () => import('./HighRisk.vue'),
    HighRiskH5: () => import('./HighRiskH5.vue'),
  },
  computed: {
    ...mapState(['IsPhone']),
  },
  data() {
    return {
      isHigh: false,
      isLow: false,
    }
  },
  mounted() {
    this.isHigh = HMarkets.length === 0
    this.isLow = LMarkets.length === 0
  },
}
</script>
<style scoped lang="scss">
.el-icon-question {
  font-size: 18px;
}
.el-icon-question:hover {
  color: #fd8465;
}
.box {
  margin: 0 auto;
  margin: 20px 0;
  width: 1200px;
}
h1 {
  font-weight: 600;
  font-size: 26px;
  color: #566570;
  .el-divider--vertical {
    width: 6px;
    height: 36px;
    border-radius: 3px;
  }
}
.high-title {
  .el-divider--vertical {
    background-color: #fd8465;
  }
}
.low-title {
  .el-divider--vertical {
    background-color: #2196f3;
  }
}

.divider {
  border-bottom: 2px dashed #939ca3;
  margin: 30px 0 15px 0;
}
.note {
  color: #566570;
  font-size: 16px;
}
.low-home {
  ul {
    border-radius: 36px;
    border: 1px solid #aab1b7;
    padding-inline-start: 0;
    background-color: rgba(255, 255, 255, 1);
    margin-bottom: 10px;
    li {
      list-style-type: none;
      padding: 5px 0;
    }
  }
  ul:hover {
    border-color: #2196f3;
    box-shadow: 0px 0px 8px #1976d23b;
  }
  ul:focus {
    border-color: #2196f3;
    box-shadow: 0px 0px 8px #1976d23b;
  }

  .title {
    padding: 10px 30px;

    .el-row {
      padding: 10px 0;
      display: flex;
      align-items: center;
      .el-divider--vertical {
        height: 52px;
      }
      // .el-col {
      //   padding: 0 10px;
      // }
      li {
        white-space: normal;
        word-break: break-all;
        word-wrap: break-word;
      }
    }
  }

  .title_img {
    width: 20%;
  }

  .title_text {
    display: flex;
    align-items: center;

    span {
      padding-left: 5px;
      font-size: 18px;
      color: rgba(86, 101, 112, 1);
    }
  }

  .top_li {
    font-size: 14px;
    color: rgba(147, 156, 163, 1);
  }

  .top_l3 {
    font-size: 14px;
    height: 25px;
    color: #566570;

    span {
      cursor: help;
    }
  }

  .top_l2 {
    font-size: 14px;
    height: 25px;
    color: #fff;
  }

  .bom_tu {
    // float: right;
    margin-left: 10px;
    color: #2196f3;
    border-bottom: 1px solid;
    font-size: 18px;
    cursor: pointer;
  }

  .bom_li {
    font-size: 18px;
    // height: 10px;
    color: rgba(86, 101, 112, 1);

    .showWbtc {
      float: right;
      font-size: 14px;
      color: #409eff;
      border-bottom: 1px solid #409eff;
      cursor: pointer;
    }
  }

  .bottom {
    padding-left: 30px;
    background: rgba(244, 249, 253, 1);
    border-radius: 0 0 36px 36px;
  }

  .body {
    padding: 30px 0;

    .el-button {
      border-radius: 30px;
    }

    .spanText {
      font-size: 14px;
      color: #939ca3;
    }
  }

  .el-button {
    width: 90%;
    font-size: 14px;
  }

  .body_text {
    .el-row {
      padding: 10px 0;
      display: flex;
      align-items: center;
    }

    .el-button {
      border-radius: 30px;
    }
  }

  .input_span {
    float: right;
    font-size: 14px;
    color: rgba(86, 101, 112, 1);
    cursor: pointer;
    margin-bottom: 5px;
  }

  .Max {
    background-color: rgba(255, 162, 103, 1);
    border-radius: 50px;
    padding: 0 10px;
    color: rgba(255, 255, 255, 1);
  }

  /deep/ .el-input-group__append {
    background-color: rgba(244, 249, 253, 1) !important;
    border: none !important;
    border-radius: 36px;
  }

  /deep/ .el-input__inner {
    border: none !important;
    background-color: rgba(244, 249, 253, 1) !important;
    border-radius: 36px;
  }

  /deep/ .el-slider__button-wrapper {
    z-index: 0 !important;
  }

  .input_li {
    // border: 1px solid rgba(204, 208, 211, 1);
    // border-radius: 36px;
    padding: 0;
    margin: 5px 0;
  }

  .el-input {
    border: 1px solid rgba(204, 208, 211, 1);
    border-radius: 36px;
  }

  // /deep/ .el-input:focus-within {
  //   border: 1px solid rgba(33, 150, 243, 1);
  //   border-radius: 36px;
  // }
  .el-input:hover {
    border: 1px solid rgba(33, 150, 243, 1);
    border-radius: 36px;
  }

  .el-input:active {
    border: 1px solid rgba(33, 150, 243, 1);
    border-radius: 36px;
  }

  /deep/ .el-slider__button {
    width: 10px;
    height: 10px;
  }
}

.el-col-10 {
  position: relative;
}

.ratio {
  position: absolute;
  bottom: 0px;
  // margin-left: 25%;
  font-size: 14px;
  color: #ffa267;
}
@media screen and (max-width: 768px) {
  .box {
    width: 90% !important;
  }
  .el-icon-question {
    font-size: 16px;
  }
  h1 {
    font-weight: 500;
    font-size: 16px;
    .el-divider--vertical {
      height: 24px;
    }
  }
}
</style>
