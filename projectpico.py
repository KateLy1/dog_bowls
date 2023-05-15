include "pico/stdlib.h"
ifndef DS18B20_H_
define DS18B20_H_
include "stm32f1xx_hal.h"
include <string.h>
include <stdlib.h>
include <stdint.h>
include "ds18b20.h"


def ds18b20_Reset(void):
    uint16_t status
    GPIOB->ODR &= ~GPIO_ODR_ODR11
    DelayMicro(485)
    GPIOB->ODR |= GPIO_ODR_ODR11
    DelayMicro(65)
    status = GPIOB->IDR & GPIO_IDR_IDR11
    DelayMicro(500)
    return (status)

def ds18b20_ReadStratcpad(mode, *Data, DevNum):
    uint8_t i
    ds18b20_Reset()
    if(mode==SKIP_ROM):
        ds18b20_WriteByte(0xCC)
    ds18b20_WriteByte(0xBE)
    for i in range(8):
        Data[i] = ds18b20_ReadByte()
        
def ds18b20_GetSign(dt):
    if (dt&(1<<11)):
        return 1
    else:
        return 0

def ds18b20_MeasureTemperCmd(mode, DevNum):
    ds18b20_Reset()
    if(mode==SKIP_ROM):
        ds18b20_WriteByte(0xCC)
    ds18b20_WriteByte(0x44)


int main() {
    dt: int8
    raw_temper: np.int16
    temper: float
    c: char
    const uint LED_PIN = PICO_DEFAULT_LED_PIN; #here is pin number
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT); #its for heatting
    on = true
    while (true) {
        ds18b20_MeasureTemperCmd(SKIP_ROM, 0)
        HAL_Delay(800)
        ds18b20_ReadStratcpad(SKIP_ROM, dt, 0)
        HAL_UART_Transmit(&huart1,(uint8_t*)str1,strlen(str1),0x1000);
        raw_temper = ((uint16_t)dt[1]<<8)|dt[0];
        if(ds18b20_GetSign(raw_temper)):
            gpio_put(LED_PIN, 1);
            sleep_ms(250);   #time will be bigger
            gpio_put(LED_PIN, 0);
    }
#endif
}
