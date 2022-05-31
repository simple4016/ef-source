package tech.yeez.investment.utils;

import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import tech.yeez.investment.SubscripterApplication;

import java.time.LocalDate;
import java.time.Month;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = SubscripterApplication.class)
public class DateUtilTest {

    @Test
    public void testAddMinute() throws Exception {
        Date result = DateUtil.addMinute(new GregorianCalendar(2022, Calendar.MAY, 26, 14, 54).getTime(), 0);
        Assert.assertEquals(new GregorianCalendar(2022, Calendar.MAY, 26, 14, 54).getTime(), result);
    }

    @Test
    public void testAddDay() throws Exception {
        Date result = DateUtil.addDay(new GregorianCalendar(2022, Calendar.MAY, 26, 14, 54).getTime(), 0);
        Assert.assertEquals(new GregorianCalendar(2022, Calendar.MAY, 26, 14, 54).getTime(), result);
    }

    @Test
    public void testGetThisDayBeginTime() throws Exception {
        String result = DateUtil.getThisDayBeginTime(LocalDate.of(2022, Month.MAY, 26));
        Assert.assertEquals("replaceMeWithExpectedResult", result);
    }

    @Test
    public void testMain() throws Exception {
        DateUtil.main(new String[]{"args"});
    }
}

//Generated with love by TestMe :) Please report issues and submit feature requests at: http://weirddev.com/forum#!/testme