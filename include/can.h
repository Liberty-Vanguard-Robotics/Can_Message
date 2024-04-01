#pragma once

#include <stdint.h>

#include "stm32f7xx_hal.h"

typedef struct {
    uint32_t id;
    uint8_t dataLength = 8;
    uint8_t data[8] = {0};
    uint32_t time;
} CAN_Message;

typedef void (*RxFifoCallback)(const CAN_Message &);

typedef struct {
    uint16_t filterId;
    uint16_t filterIdMask;
    RxFifoCallback callback;
} CAN_RxFifoConfig;


void CAN_Init(CAN_RxFifoConfig fifo0Config, CAN_RxFifoConfig fifo1Config);
bool CAN_SendMessage(const CAN_Message *TxMessage);
bool CAN_ReadRmdMessage(CAN_Message *RxMessage);
bool CAN_ReadCanOpenMessage(CAN_Message *RxMessage);

uint32_t CAN_GetTransmissionCount();
uint32_t CAN_GetReceptionCount();

uint32_t CAN_GetErrorCode();
