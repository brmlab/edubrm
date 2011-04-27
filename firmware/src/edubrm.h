void GetInReport (uint8_t src[], uint32_t length);
void SetOutReport (uint8_t dst[], uint32_t length);
void EnablePWM1(uint32_t period, uint32_t duty);
void EnablePWM2(uint16_t period, uint16_t duty);
void PinDir(uint16_t mask);
void PinState(uint8_t which, uint8_t state);
void EduInit();
void SwitchesSetup(uint8_t states);
