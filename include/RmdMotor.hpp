#pragma once

#include "Motor.hpp"
#include "CanMotor.hpp"

class RmdMotor : public CanMotor
{
public:
    static uint8_t NodeIdToMotorIndex(uint8_t nodeId);

    RmdMotor(uint8_t motorIndex, Limits limits, float angleScale = 1.0f);

    bool SetPositionTarget(float positionRad);
    bool SetSpeedLimit(float speedRadPerSec);
    
    void Stop();
    void Start();
    
    void RequestUpdate();

    int8_t GetTemperature() const;

    bool ConsumeNextMessage();

private:

    void RequestPositionStatus();
    void RequestMotorStatus2();

    bool m_positionStatusReceived = false;
    bool m_velocityStatusReceived = false;

    float m_angleScale;

    // Targets
    float m_speedRadPerSec;


    // Status
    int8_t m_temperature;
};