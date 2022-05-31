<template>
  <div class="box">
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
      <span @click="openGit('https://gitlab.com/asresearch/cff-contract-v2')">
        <img src="../assets/imgs/github@2x.png" alt />
        Gitlab</span
      >
      <span @click="openGit('https://discord.gg/cUBdGs3ehM')">
        <img src="../assets/imgs/dis.png" alt /> Discord</span
      >
    </div>
    <div class="fots">
      <span class="ear">
        Earning.Farm strongly recommends you DO NOT risk assets more than you
        can afford to lose.
      </span>
    </div>
    <audit-report :dialogVisible="dialogVisible" @closeShow="closeShow" />
  </div>
</template>

<script>
import AuditReport from './AuditReport.vue'
export default {
  components: {
    AuditReport,
  },
  data() {
    return {
      dialogVisible: false,
    }
  },
  mounted() {},
  methods: {
    closeShow(val) {
      this.dialogVisible = val
    },
    openGit(url) {
      let Win = window.open()
      Win.opener = null
      Win.location = url
    },
  },
}
</script>

<style scoped lang="scss">
.box {
  display: flex;
  width: 1200px;
  align-items: center;
  margin: 0 auto;
  height: 100%;
  flex-direction: column;
}

.fots {
  margin-top: 10px;
  text-align: left;
  width: 100%;
  .ear {
    cursor: initial;
  }

  span {
    font-size: 16px;
    color: #fff;
    margin-right: 36px;
    cursor: pointer;

    img {
      height: 18px;
      margin-bottom: -3px;
    }
  }
}

@media screen and (max-width: 768px) {
  .box {
    width: 100% !important;
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
  }
}
</style>
