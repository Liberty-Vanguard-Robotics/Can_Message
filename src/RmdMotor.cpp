#include "RmdMotor.hpp"

#include "stm32f7xx_hal.h"
#include "can.h"
#include "utility.h"
#include "status.h"
#include "serial.h"

enum class Command {
    ReadPidData					= 0x30,
    WritePidToRam				= 0x31,
    WritePidToRom				= 0x32,
    ReadAccelData				= 0x33,
    WriteAccelData				= 0x34,
    ReadEncoderData				= 0x90,
    WriteEncoderOffset			= 0x91,
    WritePositionasZero			= 0x19, // Write current position as zero to ROM
    ReadMultiTurnsAngle			= 0x92,
    ReadSingleCircleAngle		= 0x94,
    ReadStatus1andErrFlags		= 0x9A,
    ClearErrFlag				= 0x9B,
    ReadStatus2					= 0x9C,
    ReadStatus3					= 0x9D,
    MotorOff					= 0x80,
    MotorStop					= 0x81,
    MotorRunning				= 0x88,
    TorqueClosedLoop			= 0xA1,
    SpeedClosedLoop				= 0xA2,
    PositionClosedLoop1			= 0xA3,
    PositionClosedLoop2			= 0xA4,
    PositionClosedLoop3			= 0xA5,
    PositionClosedLoop4			= 0xA6,
};

uint8_t RmdMotor::NodeIdToMotorIndex(uint8_t nodeId) { return nodeId - 0x141; }


RmdMotor::RmdMotor(uint8_t motorIndex, Limits limits, float angleScale) :
    CanMotor(0x141 + motorIndex, limits),
    m_angleScale(angleScale)
{
}

bool RmdMotor::SetPositionTarget(float positionRad)
{
    if (m_isStopped) return false;

	if (positionRad < m_minAngleRad) positionRad = m_minAngleRad;
	if (positionRad > m_maxAngleRad) positionRad = m_maxAngleRad;

    int32_t positionTargetHundredthDeg = (-1) * (int32_t)(ToDegrees(positionRad) * 100.0f * m_angleScale); // NOTE: The RMD motors think there are 600 hundredths of a degree in a degree, so we multiply by 600 instead of 100
    uint16_t speedDegPerSec = (uint16_t)(ToDegrees(m_maxSpeedRadPerSec) * m_angleScale); // NOTE: The RMD motors think there are 6 degrees per second in a degree per second, so we multiply by 6

    Serial_PrintUint32(speedDegPerSec);
    Serial_PrintLine("");

    CAN_Message message;
    message.id = m_nodeId;

    message.data[0] = (uint8_t)Command::PositionClosedLoop2;
    *(uint16_t*)(message.data + 2) = speedDegPerSec;
    *(int32_t*)(message.data + 4) = positionTargetHundredthDeg;

    return SendMessage(message);
}

bool RmdMotor::SetSpeedLimit(float speedRadPerSec)
{
    if (m_isStopped) return false;



    if (speedRadPerSec > m_maxSpeedRadPerSec) speedRadPerSec = m_maxSpeedRadPerSec;
    
    m_speedRadPerSec = speedRadPerSec;
    return true;
}

void RmdMotor::Stop()
{
	m_isStopped = true;

    CAN_Message message;
    message.id = m_nodeId;
    message.data[0] = (uint8_t)Command::MotorStop;
    message.time = HAL_GetTick();
    SendMessage(message);
}

void RmdMotor::Start()
{
	m_isStopped = false;
}

void RmdMotor::RequestUpdate()
{
    RequestPositionStatus();
    RequestMotorStatus2();
}

int8_t RmdMotor::GetTemperature() const
{
    return m_temperature;
}

bool RmdMotor::ConsumeNextMessage()
{
    if (m_rxMessageQueue.empty()) return false;

    const CAN_Message &message = m_rxMessageQueue.front();
    if (message.id != m_nodeId) {
		Status_ReportError("RmdMotor tried to consume a message that didn't belong to it");
		return false;
	}

    switch ((Command)message.data[0])
    {
        case Command::ReadMultiTurnsAngle: {
            m_positionStatusReceived = true;
            int64_t angleCounts = *(int64_t *)(message.data) >> 8;
            m_positionStatusRad = (-1) * ToRadians((float)angleCounts / 100.0f / m_angleScale);
            break;
        }
        case Command::ReadStatus2: {
            m_velocityStatusReceived = true;

            m_temperature = message.data[1];
            uint16_t speedCounts = 0;
            speedCounts |= message.data[4];
            speedCounts |= message.data[5] << 8;
            break;
        }
        default:
            break;
    }
	m_rxMessageQueue.pop();
    return true;
}

void RmdMotor::RequestPositionStatus()
{
    CAN_Message message;
    message.id = m_nodeId;
    message.time = HAL_GetTick();
    message.data[0] = (uint8_t)Command::ReadMultiTurnsAngle;
    SendMessage(message);
}

void RmdMotor::RequestMotorStatus2()
{
    CAN_Message message;
    message.id = m_nodeId;
    message.dataLength = 8;
    message.time = HAL_GetTick();
    message.data[0] = (uint8_t)Command::ReadStatus2;
    SendMessage(message);
}
