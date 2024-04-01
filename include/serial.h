#pragma once

#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <string>

#include "can.h"

#define SERIAL_LINE_MAX_LENGTH (2048)

void Serial_Init();

bool Serial_IsInteractive();

void Serial_Write(const uint8_t *buffer, uint16_t size);

void Serial_Print(const char *msg);
void Serial_PrintLine(const char *msg);
std::string Serial_GetLine();

void Serial_PrintByte(uint8_t byte);
void Serial_PrintChar(char c);
void Serial_PrintInt32(int32_t value);
void Serial_PrintUint32(uint32_t value);
void Serial_PrintUint32Hex(uint32_t value);
void Serial_PrintFloatPrecision(float value, int precision);
void Serial_PrintFloat(float value);
void Serial_PrintCAN(const CAN_Message *message);
