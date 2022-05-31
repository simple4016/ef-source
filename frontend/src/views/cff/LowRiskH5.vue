<template>
  <div class="low-home">
    <ul
      v-for="(item, idx) in list"
      :key="idx"
      :class="{ 'ul-border': item.showContent }"
    >
      <div class="title">
        <el-row>
          <el-col :span="11">
            <div class="title_text">
              <img
                class="title_img"
                :src="require('../../assets/imgs/' + item.code + '.png')"
                alt
              />
              <span>{{
                item.code === 'WBTC' ? 'BTC/' + item.code : item.code
              }}</span>
            </div>
          </el-col>

          <el-col :span="2">
            <div>
              <el-divider direction="vertical"></el-divider>
            </div>
          </el-col>
          <el-col :span="12">
            <span style="font-size: 14px; color: #566570">
              APY：{{ $numFixed(item.sevendayProfit, 1) + '%' }}</span
            >
          </el-col>
          <el-col :span="1">
            <i
              :class="
                item.showContent ? 'el-icon-arrow-up' : 'el-icon-arrow-down'
              "
              style="cursor: pointer"
              @click="changeContent(item)"
            ></i>
          </el-col>
        </el-row>
      </div>

      <div v-if="item.showContent" class="bottom">
        <div class="body">
          <el-row>
            <el-col :span="6">
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  Asset: Personal total assets in USDC calculated in real time
                  based on Curve pools. Due to slipage when withdraw, number
                  withdrew would have slight difference than Asset number.
                  <br />
                  Accu Yield: Calculated based on numbers when doing yield
                  farming.
                </div>
                <span class="bom_li">Personal：</span>
              </el-tooltip>
            </el-col>
            <el-col :span="9">
              <span class="bom_li">Asset</span><br />
              <span class="spanText">{{
                $nameFixed(item.user_assets, item.code)
              }}</span>
            </el-col>
            <el-col :span="9">
              <span class="bom_li">Accu Yield</span><br />
              <span class="spanText">{{
                $nameFixed(item.user_profit, item.code)
              }}</span>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="6">
              <el-tooltip class="item" effect="dark" placement="top">
                <div slot="content">
                  7 Days APY: Calculated by the past 7 days daily APR in
                  average.
                </div>
                <span class="bom_li">Protocol：</span>
              </el-tooltip>
            </el-col>
            <el-col :span="9">
              <span class="bom_li">Asset</span><br />
              <span class="spanText">{{
                $nameFixed(item.totalassets, item.code)
              }}</span>
            </el-col>
            <el-col :span="9">
              <span class="bom_li">7 Days APY</span><br />
              <span class="spanText">{{
                $numFixed(item.sevendayProfit, 1) + '%'
              }}</span>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="6">
              <span class="bom_li">Strategy</span>
            </el-col>
            <el-col :span="18">
              <span class="spanText">{{ textList[item.code] }}</span>
              <br />
              <span class="spanText">
                {{ $feeRatio(item.feeRatio) }}% of yielding rewards will be
                charged as processing fee.
              </span>

              <div class="linetable">
                <span class="bom_tu" @click="selectLine(item)"
                  ><i class="el-icon-data-line"></i>View Trend</span
                >
                <span class="bom_tu" @click="selectTable(item)"
                  ><i class="el-icon-notebook-2"></i>View History</span
                >
              </div>
            </el-col>
          </el-row>
        </div>
        <div class="body_text">
          <div class="btcwbtc">
            <span class="bom_li">
              Wallet Balance:
              {{ $nameFixed(totalOf, item.code) }}
              <span>{{ item.code }}</span>
            </span>
          </div>
          <div class="maxinput">
            <div>
              <el-input
                v-model="confirmInput"
                @input="inputConfirm"
                @focus="Max = 1"
                onkeyup="value=value.replace(/[^\d^\.]/g,'')"
                :style="{ 'border-color': Max === 1 ? '#2196f3' : '' }"
              >
                <template slot="append">
                  <span
                    class="Max"
                    v-show="Max === 1"
                    @click="setMax(Max, totalOf)"
                    >{{ item.code === 'ETH' ? 'SAFE MAX' : 'MAX' }}</span
                  >
                </template>
              </el-input>
              <el-slider
                v-model="confirmVal"
                :step="25"
                :marks="marks"
                @change="setConfirmVal"
                show-stops
                :show-tooltip="false"
              ></el-slider>
            </div>
          </div>
          <div>
            <el-button
              type="primary"
              plain
              class="crbtn"
              v-if="item.code !== 'ETH' && isApprove"
              @click="approve"
              >Approve
            </el-button>
            <el-button
              type="primary"
              plain
              class="crbtn"
              v-else
              @click="confirm(item)"
            >
              Deposit</el-button
            >
          </div>

          <div class="btcwbtc">
            <span class="bom_li">
              Asset Deposited: ≈
              {{ $nameFixed(item.user_assets, item.code) }}
              <span>{{ item.code }}</span>
              <el-tooltip class="item" effect="dark" placement="top-end">
                <div slot="content">
                  Calculated based on Curve virtual price. May have slight
                  difference when withdrawing.
                </div>
                <i class="el-icon-question"></i>
              </el-tooltip>
            </span>
          </div>

          <div class="maxinput">
            <div>
              <el-input
                v-model="withdrawInput"
                @input="inputWithdraw"
                @focus="Max = 2"
                :style="{ 'border-color': Max === 2 ? '#2196f3' : '' }"
                onkeyup="value=value.replace(/[^\d^\.]/g,'')"
              >
                <template slot="append">
                  <span
                    class="Max"
                    v-show="Max === 2"
                    @click="setMax(Max, item)"
                    >MAX</span
                  >
                </template>
              </el-input>

              <el-slider
                v-model="withdrawVal"
                :step="25"
                :marks="marks"
                @change="setWithdrawVal"
                show-stops
                :show-tooltip="false"
              ></el-slider>
            </div>
          </div>
          <el-button
            type="primary"
            class="crbtn"
            plain
            @click="withdrawItem(item)"
          >
            Withdraw
          </el-button>

          <div class="btcwbtc">
            <span class="bom_li ratio">Fees: {{ ratio }}</span>
          </div>
        </div>
      </div>
    </ul>

    <dialog-form
      :dialogVisible="dialogVisible"
      :diaWidth="diaWidth"
      :title="title"
      @closeMain="closeMain"
      v-if="dialogVisible"
    >
      <component
        :is="currentName"
        :echartsData="echartsData"
        :codeurl="codeurl"
        :eHeight="'400px'"
        :code="itemData.code"
      />
    </dialog-form>
  </div>
</template>

<script>
import EchartsLine from './EchartsLine.vue'
import CffTable from './CffTable.vue'
import DialogForm from '../../components/DialogForm.vue'
import LowRiskMixin from '../../components/mixins/LowRiskMixin'
export default {
  name: 'LowRisk',
  mixins: [LowRiskMixin],
  components: {
    DialogForm,
    EchartsLine,
    CffTable,
  },
  computed: {
    currentName() {
      switch (this.dialogName) {
        case 'EchartsLine':
          return EchartsLine
        case 'CffTable':
          return CffTable
        default:
          return ''
      }
    },
  },
}
</script>
<style scoped lang="scss">
.crbtn {
  border-radius: 36px;
  margin-bottom: 10px;
}
.low-home {
  ul {
    border-radius: 22px;
    border: 1px solid #aab1b7;
    padding-inline-start: 0;
    background-color: #fff;
    margin-bottom: 10px;
    li {
      list-style-type: none;
      padding: 5px 0;
    }
  }
  ul:hover {
    border-color: #2196f3;
    box-shadow: 0px 0px 8px rgba(25, 118, 210, 0.23);
  }

  .ul-border {
    border-color: #2196f3;
    box-shadow: 0px 0px 8px rgba(25, 118, 210, 0.23);
  }
  .title {
    padding: 10px 14px;

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
      color: #566570;
      font-weight: 500;
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

    margin-right: 20px;
    font-size: 14px;
    color: #2196f3;
    border-bottom: 1px solid;
    cursor: pointer;
  }

  .bom_li {
    font-size: 14px;
    color: #566570;

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
    background: #f4f9fd;
    border-radius: 0 0 22px 22px;
  }

  .body {
    padding: 20px 0;
    .el-row {
      margin-bottom: 12px;
    }
    .el-button {
      border-radius: 30px;
    }
    .linetable {
      margin-top: 12px;
    }
    .spanText {
      font-size: 14px;
      color: #939ca3;
      margin-bottom: 14px;
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
    .btcwbtc {
      text-align: end;
      margin-right: 30px;
      padding-bottom: 10px;

      .ratio {
        color: #ffa267;
      }
    }

    .maxinput {
      margin-right: 30px;
      padding-bottom: 20px;

      .el-slider {
        width: 95%;
        margin: 0 auto;
      }
    }
  }

  .input_span {
    float: right;
    font-size: 14px;
    color: #566570;
    // cursor: pointer;
    margin-bottom: 5px;
  }

  .Max {
    background-color: #ffa267;
    border-radius: 50px;
    padding: 0 10px;
    color: #fff;
    cursor: pointer;
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

  .el-col-10 {
    position: relative;
  }
  .ratio {
    font-size: 14px;
    color: #ffa267;
  }
}
</style>
