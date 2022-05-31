<template>
  <div class="home">
    <el-table
      :data="tableData"
      stripe
      style="width: 100%"
      height="420"
      max-height="420"
      header-align="center"
    >
      <el-table-column type="expand" width="20" v-if="IsPhone">
        <template slot-scope="scope">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="Txn Hash：">
              <span class="tx_span" @click="open(scope.row.txh)">{{
                scope.row.txh | ellipsis
              }}</span>
            </el-form-item>
            <el-form-item label="Fee:" v-show="!codeType">
              <span>{{ $nameFixed(scope.row.fee, code) }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        prop="date"
        label="Date"
        :min-width="IsPhone ? 100 : 220"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.date | dateFormat(IsPhone) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="txh"
        label="Txn Hash"
        v-if="!IsPhone"
        min-width="120"
        align="center"
      >
        <template slot-scope="scope">
          <span class="tx_span" @click="open(scope.row.txh)">{{
            scope.row.txh
          }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="amount"
        :label="`Amount${IsPhone ? '' : '（' + code + '）'}`"
        :min-width="IsPhone ? 0 : 160"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ $nameFixed(scope.row.amount, code) }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fee"
        label="Fee"
        min-width="100"
        align="center"
        v-if="!IsPhone && !codeType"
      >
        <template slot-scope="scope">
          <span>{{ $nameFixed(scope.row.fee, code) }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="operation"
        label="Operation"
        :min-width="100"
        align="center"
      >
        <template slot-scope="scope">
          <span>
            {{ scope.row.operation }}
          </span>
        </template>
      </el-table-column>
      <!-- <el-table-column prop="flag" label="状态" width="60">
        <template slot-scope="scope">
          <i
            :class="scope.row.flag==='succes'?'el-icon-circle-check':'el-icon-circle-close'"
            :style="{color:scope.row.flag==='succes'?'#67C23A':'#F56C6C'}"
          ></i>
        </template>
      </el-table-column>-->
    </el-table>
    <el-pagination
      layout="prev, pager, next"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :total="total"
    ></el-pagination>
  </div>
</template>

<script>
import dayjs from 'dayjs'
import { mapState } from 'vuex'
import { OPEN_URL } from '../../config.js'
import { getTransaction } from '@/common/api'
export default {
  name: 'CffTable',
  props: {
    code: {
      type: String,
      default: 'USDC',
    },
    codeType: {
      type: Boolean,
      default: false,
    },
    codeurl: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      currentPage: 1,
      total: 0,
      tableData: [],
    }
  },
  computed: {
    ...mapState(['IsPhone', 'MetaMaskAddress']),
  },
  filters: {
    ellipsis(val) {
      if (!val) return ''
      if (val.length > 10) {
        return val.slice(0, 6) + '...' + val.slice(val.length - 4, val.length)
      }
      return val
    },
    dateFormat(val, phone) {
      return phone
        ? dayjs(val * 1000).format('MM-DD HH:mm')
        : dayjs(val * 1000).format('YYYY-MM-DD  HH:mm:ss')
    },
  },
  mounted() {
    this.getData()
  },
  methods: {
    async getData() {
      const query = { address: this.MetaMaskAddress, pageNo: this.currentPage }
      const list = await getTransaction(query, this.codeurl)
      if (list) {
        this.tableData = list.dataList
        if (this.currentPage === 1) {
          this.total = list.page.count
        }
      }
    },
    open(id) {
      const Win = window.open()
      Win.opener = null
      Win.location = `${OPEN_URL + id}`
    },
    handleCurrentChange(val) {
      this.getData()
    },
  },
}
</script>
<style lang="scss" scoped>
.home {
  height: 100%;
  width: 100%;
  // background: rgba(237, 246, 253, 1);
  // /deep/ .el-table th {
  //   background: rgba(237, 246, 253, 1);
  //   color: rgba(24, 130, 214, 1);
  //   font-weight: 500;
  // }

  img {
    width: 20px;
    margin-right: 10px;
  }

  .btn {
    float: right;
  }

  .tx_span {
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #2196f3;
  }

  /deep/ .el-table tr {
    background: rgba(226, 242, 255, 1);
  }

  /deep/ .el-table--striped .el-table__body tr.el-table__row--striped td {
    background: rgba(245, 249, 252, 1);
  }

  /deep/ .el-table {
    line-height: none;
  }

  /deep/ .el-table .cell {
    // display: flex;
  }

  /deep/ .el-table__empty-text {
    display: none;
  }

  /deep/ .el-pagination {
    float: right;
  }

  /deep/ .el-table__expanded-cell {
    padding: 0px;
  }

  /deep/ .el-form-item {
    margin-bottom: 0px;
  }
}
</style>
