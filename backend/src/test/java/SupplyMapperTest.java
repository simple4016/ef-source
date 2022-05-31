import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import tech.yeez.investment.SubscripterApplication;
import tech.yeez.investment.mapper.SupplyMapper;
import tech.yeez.investment.model.entity.Supply;
import tech.yeez.investment.utils.DateUtil;

import java.time.LocalDate;
import java.util.List;

/**
 * @description: test
 * @author: xiangbin
 * @create: 2022-05-18 09:32
 **/
@RunWith(SpringRunner.class)
@SpringBootTest(classes = SubscripterApplication.class)
public class SupplyMapperTest {

    @Autowired
    private SupplyMapper supplyMapper;

    @Test
    public void getSupplyLastCount(){
        LocalDate startTime = LocalDate.now();
        Integer size = 3;
        List<Supply> supplies = supplyMapper.getSupplyLastCount(DateUtil.getThisDayBeginTime(startTime), size);
        supplies.forEach(v->{
            System.out.println(v.getApy());
        });

    }
}
