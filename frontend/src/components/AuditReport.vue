<template>
  <div>
    <dialog-form
      :dialogVisible="dialogVisible"
      :diaWidth="itemWidth"
      :title="title"
      @closeShow="closeShow"
      v-if="dialogVisible"
    >
      <el-button
        type="primary"
        plain
        round
        v-for="item in audit"
        :key="item.name"
        @click="openGit(item.url)"
        >{{ item.name }}</el-button
      >
    </dialog-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import DialogForm from './DialogForm.vue'
export default {
  components: {
    DialogForm,
  },
  computed: {
    ...mapState(['IsPhone']),
    itemWidth() {
      return this.IsPhone ? '90%' : '40%'
    },
  },
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      title: 'Audit Report',
      diaWidth: '40%',
      audit: [
        {
          name: 'Low risk USDC and BTC strategy',
          url: 'https://github.com/slowmist/Knowledge-Base/blob/master/open-report/Smart%20Contract%20Security%20Audit%20Report%20-%20earning.farm.pdf',
        },
        {
          name: 'Low risk ETH strategy',
          url: 'https://github.com/slowmist/Knowledge-Base/blob/master/open-report/SlowMist%20Audit%20Report%20-%20CFFv2.pdf',
        },
        {
          name: 'High risk USDC and ETH strategy',
          url: 'https://github.com/slowmist/Knowledge-Base/blob/master/open-report-V2/smart-contract/SlowMist%20Audit%20Report%20-%20earning.farm_en-us.pdf',
        },
      ],
    }
  },
  methods: {
    closeShow() {
      this.$emit('closeShow', false)
    },

    openGit(url) {
      let Win = window.open()
      Win.opener = null
      Win.location = url
    },
  },
}
</script>

<style lang="scss" scoped>
.el-button {
  width: 100%;
  display: block;
  margin: 15px auto;
}
</style>
