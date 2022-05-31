import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import tech.yeez.investment.SubscripterApplication;
import tech.yeez.investment.model.entity.TransactionRecord;
import tech.yeez.investment.model.vo.TransactionVo;
import tech.yeez.investment.service.ITransactionRecordService;

import java.util.List;
import java.util.stream.Collectors;

/**
 * @description: test
 * @author: xiangbin
 * @create: 2022-04-21 17:06
 **/

@RunWith(SpringRunner.class)
@SpringBootTest(classes = SubscripterApplication.class)
public class TransactionRecordServiceTest {

    @Autowired
    private ITransactionRecordService transactionRecordService;


    @Test
    public void findForPage(){
        Page<TransactionRecord> page = new Page<>(10, 2);
        String address = "123";
        Page<TransactionRecord> transactionRecordPage =  transactionRecordService.findTranForPage(page, address);
        List<TransactionVo> transactionVos = transactionRecordPage.getRecords().stream().map(TransactionVo::transfer).collect(Collectors.toList());
        for (TransactionVo transactionVo : transactionVos) {
            System.out.println(transactionVo.getAmount());
        }
        for (TransactionRecord record : transactionRecordPage.getRecords()) {
            System.out.println(record.getId());
        }
    }


}
