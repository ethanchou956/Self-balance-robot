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
#define ACCEL_XOUT_H 0x3B

int main()
{
    stdio_init_all();

    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);

    uint8_t buf[] = {0x6B, 0x80};
    i2c_write_blocking(I2C_PORT, MPU6050_ADDR, buf, 2, false);
    sleep_ms(100);

    buf[1] = 0x00;
    i2c_write_blocking(I2C_PORT, MPU6050_ADDR, buf, 2, false);
    sleep_ms(100);

    uint8_t accel_config[] = {0x1C, 0x00};
    i2c_write_blocking(I2C_PORT, MPU6050_ADDR, accel_config, 2, false);
    sleep_ms(100);

    uint8_t reg = 0x75;
    uint8_t who;
    i2c_write_blocking(I2C_PORT, MPU6050_ADDR, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, MPU6050_ADDR, &who, 1, false);
    printf("WHO_AM_I = 0x%02X\n", who);

    while (true) {
        int16_t accel[3];
        uint8_t buffer[6];

        // Start reading acceleration registers from register 0x3B for 6 bytes
        uint8_t val = 0x3B;

        i2c_write_blocking(I2C_PORT, MPU6050_ADDR, &val, 1, true);
        i2c_read_blocking(I2C_PORT, MPU6050_ADDR, buffer, 6, false);

        for (int i = 0; i < 3; i++) {
            accel[i] = (buffer[i * 2] << 8 | buffer[(i * 2) + 1]);
        }

        float gx = accel[0] / 16384.0;
        float gy = accel[1] / 16384.0;
        float gz = accel[2] / 16384.0;

        printf("X=%.2fG  Y=%.2fG  Z=%.2fG\n", gx, gy, gz);

        sleep_ms(1000);
    }
}
