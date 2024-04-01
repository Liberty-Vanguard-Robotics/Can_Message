#include "serial.h"

#include "stm32f7xx_hal.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "status.h"
#include "ftoa.h"

#include "can.h"

UART_HandleTypeDef huart3;
DMA_HandleTypeDef hdma_usart3_rx;

char mainBuf[SERIAL_LINE_MAX_LENGTH + 1];
char rxBuf[SERIAL_LINE_MAX_LENGTH + 1];
int messageSize = 0;

void Serial_Init() {
	/* DMA controller clock enable */
	__HAL_RCC_DMA1_CLK_ENABLE();

	/* DMA interrupt init */
	/* DMA1_Stream1_IRQn interrupt configuration */
	HAL_NVIC_SetPriority(DMA1_Stream1_IRQn, 0, 0);
	HAL_NVIC_EnableIRQ(DMA1_Stream1_IRQn);

	__HAL_DMA_DISABLE_IT(&hdma_usart3_rx, DMA_IT_HT);


    huart3.Instance = USART3;
    huart3.Init.BaudRate = 115200;
    huart3.Init.WordLength = UART_WORDLENGTH_8B;
    huart3.Init.StopBits = UART_STOPBITS_1;
    huart3.Init.Parity = UART_PARITY_NONE;
    huart3.Init.Mode = UART_MODE_TX_RX;
    huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart3.Init.OverSampling = UART_OVERSAMPLING_16;
    huart3.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
    huart3.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
    ASSERT(HAL_UART_Init(&huart3) == HAL_OK);

	messageSize = 0;

	HAL_UARTEx_ReceiveToIdle_DMA(&huart3, (uint8_t *) rxBuf, SERIAL_LINE_MAX_LENGTH);
}

void Serial_Write(const uint8_t *buffer, uint16_t size) {
	HAL_UART_Transmit(&huart3, (uint8_t *)buffer, size, HAL_MAX_DELAY);
}

void Serial_Print(const char * msg) {
	Serial_Write((uint8_t*)msg, strlen(msg));
}

void Serial_PrintLine(const char * msg) {
	Serial_Print(msg);
	Serial_Print("\r\n");
}

std::string Serial_GetLine()
{
	if (messageSize > 0)
		return mainBuf;
	else
		return "";
}

void Serial_PrintByte(uint8_t value) {
	char msg[3];
	sprintf(msg, "%.2x", value);
	Serial_Print(msg);
}

void Serial_PrintChar(char c) {
	HAL_UART_Transmit(&huart3, (uint8_t*)&c, 1, HAL_MAX_DELAY);
}

void Serial_PrintInt32(int32_t value) {
	char msg[11];
	sprintf(msg, "%d", value);
	Serial_Print(msg);
}

void Serial_PrintUint32(uint32_t value) {
	char msg[11];
	sprintf(msg, "%u", value);
	Serial_Print(msg);
}

void Serial_PrintUint32Hex(uint32_t value) {
	char msg[11];
	sprintf(msg, "%x", value);
	Serial_Print(msg);
}

void Serial_PrintFloat(float value) {
	Serial_PrintFloatPrecision(value, 2);
}

void Serial_PrintFloatPrecision(float value, int precision) {
	char msg[64];
	ftoa(value, msg, precision);
	Serial_Print(msg);
}

void Serial_PrintCAN(const CAN_Message *message)
{
	uint8_t bytes = message->dataLength;

	Serial_Print("{0x");

	if (message->id & 0xFFFF0000) {
		Serial_PrintByte(message->id >> 24);
		Serial_PrintByte(message->id >> 16);
	}
	Serial_PrintByte(message->id >> 8);
	Serial_PrintByte(message->id);
	Serial_Print(":");

	if (bytes > 8) bytes = 8;
	
	for (int i = 0; i < bytes; i++)
	{
		Serial_Print(" ");
		Serial_PrintByte(message->data[i]);
	}
	Serial_Print("}");
}

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
	if (huart->Instance == USART3)
	{
		memcpy ((uint8_t *)mainBuf, rxBuf, Size);
		messageSize = Size;
		mainBuf[messageSize] = '\0';

		HAL_UARTEx_ReceiveToIdle_DMA(&huart3, (uint8_t *)rxBuf, SERIAL_LINE_MAX_LENGTH);
		__HAL_DMA_DISABLE_IT(&hdma_usart3_rx, DMA_IT_HT);
	}
}
