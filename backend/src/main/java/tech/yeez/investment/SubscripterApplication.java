package tech.yeez.investment;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.ConfigurableApplicationContext;
import tech.yeez.investment.utils.SpringBeanUtil;

/**
 * @description: Application
 * @author: xiangbin
 * @create: 2022-04-07 16:47
 **/
@SpringBootApplication
@MapperScan("tech.yeez.investment.mapper")
@EnableFeignClients(basePackages = {"tech.yeez.investment.service.feign"})
public class SubscripterApplication {

    public static void main(String[] args) {
        ConfigurableApplicationContext configurableApplicationContext = SpringApplication.run(SubscripterApplication.class, args);

        SpringBeanUtil.applicationContext = configurableApplicationContext;
    }
}
