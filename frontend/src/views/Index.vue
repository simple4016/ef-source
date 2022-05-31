<template>
  <div class="home">
    <el-container>
      <el-header>
        <div class="header">
          <img src="../assets/imgs/logo_top@2x.png" alt />
          <div style="margin-left: auto" class="dappa">
            <el-button type="primary" @click="gohome" round>DAPP</el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <div class="body">
          <div class="icons">
            <img src="../assets/imgs/icons.png" alt="" />
          </div>
          <div class="text">
            <h2>About ENF</h2>
            <el-divider></el-divider>
          </div>
          <p class="pp">
            Vision of Earning.Farm is to provide user-friendly investment tools
            for mass population to enjoy the innovation of DEFI.
          </p>
          <p class="pp">We are providing USDC, WBTC, ETH strategy as:</p>
          <div class="ppb">
            <div v-if="lowList.length > 0">
              <p
                class="lowp"
                v-for="(item, idx) in lowList"
                :key="idx"
                @click="goCff(item, 'low')"
              >
                {{ item.code }}
                <span>
                  {{ $numFixed(item.sevendayProfit, 1) + '%' }}
                </span>
                <svg-icon iconClass="low" class="websvg"></svg-icon>
              </p>
            </div>
            <div v-if="highList.length > 0">
              <p
                v-for="(item, idx) in highList"
                :key="idx"
                @click="goCff(item, 'high')"
                style="cursor: pointer"
              >
                {{ item.code }}
                <span v-show="item.code === 'ETH'" class="leve">Leveraged</span>
                <span> {{ $numFixed(item.sevendayProfit, 1) + '%' }}</span>
                <svg-icon iconClass="high" class="websvg"></svg-icon>
              </p>
            </div>
          </div>
          <div class="dapps">
            <el-button class="dapp" type="primary" @click="gohome" round
              >DAPP</el-button
            >
          </div>
          <div class="text">
            <h2>Why ENF？</h2>
            <el-divider></el-divider>
          </div>
          <div class="cards">
            <div class="card1">
              <div class="cardsi">
                <img src="../assets/imgs/card1.png" alt="" />
                <p>Simple</p>
                <span>
                  Simplified USDC/WBTC/ETH in and out, forget about complex LP
                  tokens. Chasing high yield automatically, no need moving
                  between protocols manually.
                </span>
              </div>
            </div>
            <div class="card2">
              <div class="cardsi">
                <img src="../assets/imgs/card2.png" alt="" />
                <p>Low Risk</p>
                <span
                  >Audited by Slowmist and PeckShield. Always select proven DEFI
                  protocols and mature pools.</span
                >
              </div>
            </div>
            <div class="card3">
              <div class="cardsi">
                <img src="../assets/imgs/card3.png" alt="" />
                <p>Save Cost</p>
                <span>
                  Aggregation of farming save gas cost than operating
                  individually.
                </span>
              </div>
            </div>
          </div>
          <el-divider></el-divider>
          <div class="fots">
            <span @click="dialogVisible = true">Audit Report</span>
            <!-- <span
              @click="
                openGit(
                  'https://github.com/slowmist/Knowledge-Base/blob/master/open-report/Smart%20Contract%20Security%20Audit%20Report%20-%20earning.farm.pdf'
                )
              "
            >
              Slowmist Audit Report
            </span>
            <span
              @click="
                openGit(
                  `https://github.com/slowmist/Knowledge-Base/blob/master/open-report/SlowMist%20Audit%20Report%20-%20CFFv2.pdf`
                )
              "
            >
              PeckShield Audit Report
            </span> -->
            <span
              @click="openGit('https://gitlab.com/asresearch/cff-contract-v2')"
            >
              <img src="../assets/imgs/github@2x.png" alt />
              Gitlab
            </span>
            <span @click="openGit('https://discord.gg/cUBdGs3ehM')">
              <img src="../assets/imgs/discord@2x.png" alt /> Discord</span
            >
          </div>
          <div class="fots">
            <span class="ear"
              >Earning.Farm strongly recommends you DO NOT risk assets more than
              you can afford to lose.</span
            >
          </div>
        </div>
      </el-main>
    </el-container>
    <audit-report :dialogVisible="dialogVisible" @closeShow="closeShow" />
  </div>
</template>

<script>
import { getSevendayProfit } from '@/common/api'
import { HMarkets, LMarkets } from '../config.js'
import AuditReport from '../components/AuditReport.vue'
export default {
  name: 'Index',
  components: {
    AuditReport,
  },
  data() {
    return {
      lowList: [],
      highList: [],
      dialogVisible: false,
    }
  },
  mounted() {
    this.getSevendayProfits()
  },
  methods: {
    goCff(item, type) {
      this.$router.push({
        name: 'invest',
        params: {
          code: item.code,
          type: type,
        },
      })
    },
    async getSevendayProfits() {
      const h = HMarkets.map((item) => 'h' + item)
      const all = [...LMarkets, ...h]
      console.log(all, '=-')
      Promise.all(
        // LMarkets.map((item) => {
        // 	return getSevendayProfit(item)
        // })
        all.map((item) => {
          return getSevendayProfit(item)
        })
      )
        .then(([...all]) => {
          this.lowList = all
            .filter((item) => item.data.risk_tpye === 0)
            .map((item) => item.data)
          this.highList = all
            .filter((item) => item.data.risk_tpye === 1)
            .map((item) => item.data)
        })
        .catch((err) => {
          console.log(err, '=-')
        })
    },

    closeShow(val) {
      this.dialogVisible = val
    },
    openGit(url) {
      let Win = window.open()
      Win.opener = null
      Win.location = url
    },
    gohome() {
      this.$router.push({
        path: '/invest',
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.home {
  height: 100%;
  width: 100%;
  background: url('~@/assets/imgs/bg.png') no-repeat center bottom;
  background-size: cover;
}

.el-header {
  height: 80px !important;
  padding: 0 !important;
  box-sizing: none !important;
  font-size: 28px;
  color: rgba(86, 101, 112, 1);
  background: transparent;
  display: flex;
  justify-content: center;

  .header {
    width: 90%;
    display: flex;
    align-items: center;
    width: 1200px;

    img {
      height: 50px;
    }

    .el-button {
      width: 150px;
    }

    .el-dropdown {
      margin-left: 10px;

      .el-button {
        width: 150px;
      }
    }
  }
}

.el-main {
  padding: 0 !important;
  box-sizing: none !important;
  background-color: transparent;

  .body {
    height: 100%;
    width: 90%;
    margin: auto;
    width: 1200px;

    p {
      color: #566570;
      font-size: 20px;
      text-align: center;
    }

    .ppb {
      display: flex;
      margin-top: 20px;
      justify-content: center;
      div {
        margin: 0 20px;
        min-width: 400px;
        .lowp {
          margin-left: 80px;
        }
        p {
          // cursor: pointer;
          font-weight: 500;
          color: #566570;
          display: flex;
          align-items: center;
          padding: 10px;
          .leve {
            border: 1px solid #2196f3;
            color: #2196f3;
            font-size: 12px;
            padding: 3px 10px;
            margin: 0 10px;
            border-radius: 4px;
          }
          span {
            padding: 0 20px;
            font-size: 26px;
            color: #566570;
            font-weight: 500;
          }
          .svg-icon {
            font-size: 66px;
            margin-top: -40px;
          }
        }
      }
    }

    .fots {
      margin-bottom: 20px;
      padding: 0 20px;
      .ear {
        cursor: initial;
      }

      span {
        font-size: 16px;
        color: #566570;
        margin-right: 36px;
        cursor: pointer;

        img {
          height: 18px;
          margin-bottom: -3px;
        }
      }
    }

    .cards {
      display: flex;
      margin-bottom: 50px;

      div {
        width: 320px;
        border-radius: 38px;
        height: 380px;

        span {
          font-size: 18px;
          color: #566570;
          display: block;
          padding: 0 36px;
          // margin-bottom: 36px;
        }

        .cardsi {
          text-align: center;
          img {
            margin-top: 42px;
            height: 76px;
          }
        }
      }

      .card1 {
        background: rgba(255, 186, 168, 0.4);

        p {
          font-size: 22px;
          color: #fd8465;
        }
      }

      .card2 {
        margin: auto;
        background: rgba(139, 198, 248, 0.4);

        p {
          font-size: 22px;
          color: #21c3f3;
        }
      }

      .card3 {
        background: rgba(255, 172, 229, 0.4);

        p {
          font-size: 22px;
          color: #ff719d;
        }
      }
    }

    .dapps {
      margin-top: 40px;
      margin-bottom: 60px;

      .dapp {
        display: block;
        margin: auto;
        width: 319px;
        height: 76px;
        font-size: 24px;
        border-radius: 38px;
        box-shadow: 0px 0px 20px #2196f3;
      }
    }

    .icons {
      text-align: center;
      margin-top: 60px;

      img {
        height: 125px;
      }
    }

    .text {
      text-align: center;
      margin-bottom: 30px;

      /deep/ .el-divider--horizontal {
        width: 70px;
        margin: auto;
        margin-top: -20px;
        height: 3px;
        /* color: #2196F3; */
        background-color: #2196f3;
        border-radius: 6px;
      }

      h2 {
        font-size: 36px;
        color: #566570;
        font-weight: 400;
      }
    }
  }
}

.en {
  display: flex;
  align-items: center;
  margin-left: 20px;
  cursor: pointer;
  font-size: 14px;

  img {
    height: 24px !important;
    margin-right: 10px;
  }
}

@media screen and (max-width: 768px) {
  .body {
    width: 100% !important;
  }
  .el-header .header {
    width: 96% !important;
  }
  .ppb {
    flex-direction: column;
    align-items: center;
    div {
      min-width: 200px !important;
      .lowp {
        margin: 10px 0px !important;
      }
      p {
        justify-content: center;
        font-size: 18px !important;
        span {
          font-size: 20px !important;
          padding: 0 10px !important;
        }
        .svg-icon {
          font-size: 46px !important;
        }
        .leve {
          font-size: 12px !important;
        }
      }
    }
  }
  // .dappa {
  // 	display: none;
  // }
  .dapp {
    width: 280px !important;
    height: 46px !important;
  }
  .en {
    margin-left: auto;
  }

  .body {
    .pp {
      font-size: 16px !important;
    }
  }

  .cards {
    flex-direction: column;

    div {
      margin: auto;

      width: 340px !important;
      // height: auto !important;
    }

    .card1,
    .card2,
    .card3 {
      margin-bottom: 36px !important;
    }
  }
  .fots {
    text-align: center;
    // display: flex;
    margin-bottom: 10px !important;
    span {
      display: block;
      margin-right: 0px !important;
      margin-bottom: 10px;
    }

    .ear {
      width: 100%;
      margin: 0px !important;
      margin-bottom: 10px !important;
      text-align: left;
    }
  }
  // .fots {
  // 	text-align: center;
  // 	display: flex;
  // 	margin: 0 auto !important;
  // 	justify-content: center;
  // 	span {
  // 		margin: 0px;
  // 		margin: 0px 10px;
  // 		margin-bottom: 5px;
  // 	}

  // 	.ear {
  // 		width: 100%;
  // 		margin: 10px 0px !important;
  // 	}
  // }
}
</style>
