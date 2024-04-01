#include "can.h"

#include <stdint.h>

#include "serial.h"
#include "status.h"
#include "stm32f7xx_hal.h"

#include "can_buf.h"

CAN_HandleTypeDef hcan1;

#define TX_BUF_LEN (128)
#define RMD_RX_BUF_LEN (128)
#define CO_RX_BUF_LEN (128)

static CAN_Message TxBufArray[TX_BUF_LEN];
static CAN_Message RMD_RxBufArray[RMD_RX_BUF_LEN];
static CAN_Message CO_RxBufArray[CO_RX_BUF_LEN];

static CAN_Buffer TxBuf;
static CAN_Buffer RMD_RxBuf;
static CAN_Buffer CO_RxBuf;

static uint32_t transmissionCount = 0;
static uint32_t receptionCount = 0;

static uint32_t CAN_ErrorCount = 0;


RxFifoCallback fifo0Callback;
RxFifoCallback fifo1Callback;

void InitBuffers()
{
	CanBuf_Init(&TxBuf, TxBufArray, TX_BUF_LEN);
	CanBuf_Init(&RMD_RxBuf, RMD_RxBufArray, RMD_RX_BUF_LEN);
	CanBuf_Init(&CO_RxBuf, CO_RxBufArray, CO_RX_BUF_LEN);
}

void CAN_StartTransmission();

void CAN_Init(CAN_RxFifoConfig fifo0Config, CAN_RxFifoConfig fifo1Config)
{
	fifo0Callback = fifo0Config.callback;
	fifo1Callback = fifo1Config.callback;

	transmissionCount = 0;
	receptionCount = 0;
	CAN_ErrorCount = 0;
	InitBuffers();

	hcan1 = {};
	hcan1.Instance = CAN1;
	hcan1.Init.Prescaler = 1;
	hcan1.Init.Mode = CAN_MODE_NORMAL;
	hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
	hcan1.Init.TimeSeg1 = CAN_BS1_3TQ;
	hcan1.Init.TimeSeg2 = CAN_BS2_4TQ;
	hcan1.Init.TimeTriggeredMode = DISABLE;
	hcan1.Init.AutoBusOff = ENABLE;
	hcan1.Init.AutoWakeUp = DISABLE;
	hcan1.Init.AutoRetransmission = ENABLE;
	hcan1.Init.ReceiveFifoLocked = DISABLE;
	hcan1.Init.TransmitFifoPriority = ENABLE;
	ASSERT(HAL_CAN_Init(&hcan1) == HAL_OK);

	CAN_FilterTypeDef sFilterConfig;

	sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
	sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
	sFilterConfig.FilterActivation = ENABLE;
	sFilterConfig.SlaveStartFilterBank = 14;

	sFilterConfig.FilterBank = 0;
	sFilterConfig.FilterIdHigh = fifo0Config.filterId << 5;
	sFilterConfig.FilterIdLow = 0;
	sFilterConfig.FilterMaskIdHigh = fifo0Config.filterIdMask << 5;
	sFilterConfig.FilterMaskIdLow = 0;
	sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
	HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig);

	sFilterConfig.FilterBank = 1;
	sFilterConfig.FilterIdHigh = fifo1Config.filterId << 5;
	sFilterConfig.FilterIdLow = 0;
	sFilterConfig.FilterMaskIdHigh = fifo1Config.filterIdMask << 5;
	sFilterConfig.FilterMaskIdLow = 0;
	sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO1;
	HAL_CAN_ConfigFilter(&hcan1, &sFilterConfig);

	ASSERT(HAL_CAN_Start(&hcan1) == HAL_OK);

	ASSERT(HAL_CAN_ActivateNotification(&hcan1,
		CAN_IT_ERROR |
		CAN_IT_TX_MAILBOX_EMPTY |
		CAN_IT_RX_FIFO0_MSG_PENDING |
		CAN_IT_RX_FIFO1_MSG_PENDING) == HAL_OK);

	return;
}

bool CAN_SendMessage(const CAN_Message *TxMessage)
{
	if (CanBuf_Full(&TxBuf)) {
		Status_ReportError("CAN Tx Buffer Full");
		return false;
	}
	CanBuf_Put(&TxBuf, *TxMessage);

	CAN_StartTransmission();
	return true;
}

bool CAN_ReadRmdMessage(CAN_Message *RxMessage)
{
	return CanBuf_Get(&RMD_RxBuf, RxMessage);
}

bool CAN_ReadCanOpenMessage(CAN_Message *RxMessage)
{
	return CanBuf_Get(&CO_RxBuf, RxMessage);
}

uint32_t CAN_GetTransmissionCount() { return transmissionCount; }
uint32_t CAN_GetReceptionCount() { return receptionCount; }

uint32_t CAN_GetErrorCode() { return hcan1.ErrorCode; }

// Prompt a new transmission if no transmission is currently occurring
void CAN_StartTransmission()
{
	CAN_Message messageToSend;
	if (!CanBuf_Get(&TxBuf, &messageToSend) || HAL_CAN_GetTxMailboxesFreeLevel(&hcan1) == 0) return;

	CAN_TxHeaderTypeDef header;
	header.IDE = CAN_ID_STD;
	header.StdId = messageToSend.id;
	header.DLC = messageToSend.dataLength;

	header.RTR = CAN_RTR_DATA;
	header.TransmitGlobalTime = DISABLE;
	header.ExtId = 0;

	uint32_t mailbox = (uint32_t)(-1);
	if (HAL_CAN_AddTxMessage(&hcan1, &header, messageToSend.data, &mailbox) != HAL_OK) {
		Status_ReportError("Failed to add TX message");
	}
	else {
		// Serial_Print("Sent: ");
		// Serial_PrintCAN(&messageToSend);
		// Serial_Print(" Mailbox ");
		// Serial_PrintByte(mailbox);
		// Serial_PrintLine("");
	}
}

// TX Mailbox Callbacks
void HAL_CAN_TxMailbox0CompleteCallback(CAN_HandleTypeDef *hcan)
{
	transmissionCount++;
	Status_ToggleGreenLed();
	if (hcan == &hcan1)
		CAN_StartTransmission();
}
void HAL_CAN_TxMailbox1CompleteCallback(CAN_HandleTypeDef *hcan)
{
	transmissionCount++;
	Status_ToggleGreenLed();
	if (hcan == &hcan1)
		CAN_StartTransmission();
}
void HAL_CAN_TxMailbox2CompleteCallback(CAN_HandleTypeDef *hcan)
{
	transmissionCount++;
	Status_ToggleGreenLed();
	if (hcan == &hcan1)
		CAN_StartTransmission();
}

// RX FIFO Callbacks
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
	Status_ToggleGreenLed();

	do {
		CAN_Message receivedMessage;
		receivedMessage.time = HAL_GetTick();

		CAN_RxHeaderTypeDef header;
		if (HAL_CAN_GetRxMessage(hcan, 0, &header, receivedMessage.data) != HAL_OK) {
			Status_ReportError("Could not get Rx Message");
			return;
		}

		if (header.IDE == CAN_ID_EXT) receivedMessage.id = header.ExtId;
		else receivedMessage.id = header.StdId;

		receivedMessage.dataLength = header.DLC;

		fifo0Callback(receivedMessage);
		// if (CanBuf_Put(&RMD_RxBuf, receivedMessage)) receptionCount++;
	} while (HAL_CAN_GetRxFifoFillLevel(hcan, 0) > 0);
}

void HAL_CAN_RxFifo1MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
	Status_ToggleBlueLed();
	
	do {
		CAN_Message receivedMessage;
		receivedMessage.time = HAL_GetTick();

		CAN_RxHeaderTypeDef header;
		if (HAL_CAN_GetRxMessage(hcan, 1, &header, receivedMessage.data) != HAL_OK) {
			Status_ReportError("Could not get Rx Message");
			return;
		}

		if (header.IDE == CAN_ID_EXT) receivedMessage.id = header.ExtId;
		else receivedMessage.id = header.StdId;

		receivedMessage.dataLength = header.DLC;

		fifo1Callback(receivedMessage);
		// if (CanBuf_Put(&CO_RxBuf, receivedMessage))	receptionCount++;
	} while (HAL_CAN_GetRxFifoFillLevel(hcan, 1) > 0);
}



// Error Callback
void HAL_CAN_ErrorCallback(CAN_HandleTypeDef *hcan)
{
	CAN_ErrorCount++;
	Status_ReportError("CAN Error");
}
