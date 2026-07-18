#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define I2C_PORT i2c0
#define I2C_SDA 4   
#define I2C_SCL 5   

#define MPU6050_ADDR 0x68


int main()
{
    stdio_init_all();

    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);
    // For more examples of I2C use see https://github.com/raspberrypi/pico-examples/tree/master/i2c
    
    while (true) {
        uint8_t reg = 0x75;           
        uint8_t buffer[1];

        i2c_write_blocking(I2C_PORT, MPU6050_ADDR, &reg, 1, true);
        
        i2c_read_blocking(I2C_PORT, MPU6050_ADDR, buffer, 1, false);
       
        printf("WHO_AM_I = 0x%02X\n", buffer[0]);

        sleep_ms(1000);
    }
}
