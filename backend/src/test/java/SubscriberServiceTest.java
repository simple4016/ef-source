import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import tech.yeez.investment.SubscripterApplication;
import tech.yeez.investment.mapper.TransactionRecordMapper;

/**
 * @description: test
 * @author: xiangbin
 * @create: 2022-04-14 15:11
 **/
@RunWith(SpringRunner.class)
@SpringBootTest(classes = SubscripterApplication.class)
public class SubscriberServiceTest {

    @Autowired
    private TransactionRecordMapper transactionRecordMapper;


    @Test
    public void findAllOpenSub(){
        int a = transactionRecordMapper.updateTransactionProfit(2);
        System.out.println(a);
    }
}
