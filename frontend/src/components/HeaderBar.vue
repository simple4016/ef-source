<template>
  <div class="box">
    <img src="../assets/imgs/logo_top@2x.png" alt @click="goIndex" />
    <!-- <div class="addinput">
			<el-input
				v-model="addressInput"
				placeholder="请输入查询地址"
				v-if="Network !== 1"
			></el-input>
			<el-button
				style="width: 80px"
				class="testbtn"
				v-if="Network !== 1"
				type="text"
				@click="setAddress"
				>查询</el-button
			>
		</div> -->
    <div style="margin-left: auto" class="rightbtn">
      <el-tooltip
        class="item"
        content="Gas fee high, not recommend making deposit or withdraw."
        placement="bottom"
        effect="light"
        v-if="gasprice > 100"
      >
        <span class="gaspeice">
          <svg-icon iconClass="fei"></svg-icon> {{ gasprice }}
        </span>
      </el-tooltip>
      <span class="gaspeice" v-else
        ><svg-icon iconClass="fei"></svg-icon> {{ gasprice }}
      </span>
      <el-button
        type="primary"
        round
        @click="jump"
        v-if="MetaMaskAddress === ''"
        >Connect Wallet</el-button
      >
      <el-dropdown
        @command="handleCommand"
        trigger="click"
        placement="bottom-start"
        size="small"
        v-if="MetaMaskAddress !== ''"
      >
        <el-button
          type="primary"
          round
          :style="{ background: '#FFF', color: 'rgba(86, 101, 112, 1)' }"
        >
          {{ MetaMaskAddress | ellipsis }}
          <i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="copy">Copy Address</el-dropdown-item>
          <el-dropdown-item command="exit">Exit</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import WalletMixin from './dialog-wallet/WalletMixin'
import { mapState, mapMutations } from 'vuex'
import { copys } from '@/utils'
import { getGasPrice } from '@/common/web3'
import { Network } from '../config.js'

export default {
  mixins: [WalletMixin],
  data() {
    return {
      gasprice: 50,
      timer: null,
      addressInput: '',
    }
  },
  computed: {
    ...mapState(['MetaMaskAddress']),
  },
  filters: {
    ellipsis(val) {
      if (!val) return ''
      if (val.length > 10) {
        return val.slice(0, 6) + '...' + val.slice(val.length - 4, val.length)
      }
      return val
    },
  },
  mounted() {
    console.log(Network, 'Network')
    this.startTimer()
    this.getGasPriced()
  },
  methods: {
    ...mapMutations(['setMetaMaskAddress']),
    setAddress() {
      this.setMetaMaskAddress(this.addressInput)
      if (!this.addressInput) this.resetApp()
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.getGasPriced
      }, 10000)
    },
    async getGasPriced() {
      const price = await getGasPrice()
      console.log(price, 'priceprice')
      this.gasprice = Math.floor(price / 1e9)
    },
    goIndex() {
      this.$router.push({
        path: '/index',
      })
    },
    handleCommand(command) {
      switch (command) {
        case 'copy':
          copys(this, this.MetaMaskAddress)
          break
        case 'exit':
          this.resetApp()
          break
        default:
          break
      }
    },
    openHash(id) {
      const Win = window.open()
      Win.opener = null
      Win.location = this.tag
        ? `https://ropsten.etherscan.io/tx/${id}`
        : `https://etherscan.io/tx/${id}`
    },
    jump() {
      this.login()
    },
  },
  destroyed() {
    clearInterval(this.timer)
    this.timer = null
  },
}
</script>

<style scoped lang="scss">
.addinput {
  width: 50%;
  display: flex;
  margin-left: 30px;
}
.el-button {
  width: 150px;
  height: 40px;
}
.box {
  display: flex;
  width: 1200px;
  align-items: center;
  margin: auto 0;
  height: 100%;
  img {
    height: 50px;
    cursor: pointer;
  }
  .gaspeice {
    color: #409eff;
    font-size: 14px;
    margin: 0 10px;
    cursor: default;
  }
}
@media screen and (max-width: 768px) {
  .box {
    width: 100% !important;
    .addinput {
      display: none !important;
    }
    img {
      margin-left: 16px;
    }
    .rightbtn {
      margin-right: 16px;
    }
    .el-button {
      width: 130px !important;
      padding: 10px !important;
    }
  }
}
</style>
