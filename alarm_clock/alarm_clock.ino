#include <SevSeg.h>
#include "Button.h"
#include "AlarmTone.h"
#include "Clock.h"
#include "config.h"

const int PIN_DOTS = 13;
const int PIN_BUZZER = A3;

Button btnHour(A0);
Button btnMin(A1);
Button btnAlarm(A2);

AlarmTone soundModule;
Clock watchCore;
SevSeg display4Digit;

enum ViewMode {
  MODE_SHOW_TIME,
  MODE_ALARM_SET,
  MODE_ALARM_RINGING,
  MODE_SNOOZE_CONFIRM
};

ViewMode currentMode = MODE_SHOW_TIME;
unsigned long timestampModeChanged = 0;

void updateDisplay();
void handleTimeView();
void handleAlarmSetView();
void handleRingingView();
void handleSnoozeView();
void switchViewMode(ViewMode targetMode);
unsigned long getDurationInCurrentMode();
void toggleDots(bool turnOn);


void setup() {
  Serial.begin(115200);
  watchCore.begin();

  btnHour.begin();
  btnHour.set_repeat(500, 200);

  btnMin.begin();
  btnMin.set_repeat(500, 200);

  btnAlarm.begin();
  btnAlarm.set_repeat(1000, -1);

  soundModule.begin(PIN_BUZZER);
  pinMode(PIN_DOTS, OUTPUT);

  byte totalDigits = 4;
  byte gridPins[] = {2, 3, 4, 5};
  byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12};
  
  bool limitResistorsOnSegments = false;
  bool useDelaysUpdate = false;
  bool keepZeroes = true;
  bool hideDecimalPoint = true;
  
  display4Digit.begin(DISPLAY_TYPE, totalDigits, gridPins, segmentPins, 
                      limitResistorsOnSegments, useDelaysUpdate, keepZeroes, hideDecimalPoint);
  display4Digit.setBrightness(90);
}

void loop() {
  display4Digit.refreshDisplay();

  switch (currentMode) {
    case MODE_SHOW_TIME:      handleTimeView();        break;
    case MODE_ALARM_SET:       handleAlarmSetView();    break;
    case MODE_ALARM_RINGING:   handleRingingView();     break;
    case MODE_SNOOZE_CONFIRM:  handleSnoozeView();      break;
  }
}



void switchViewMode(ViewMode targetMode) {
  currentMode = targetMode;
  timestampModeChanged = millis();
}

unsigned long getDurationInCurrentMode() {
  return millis() - timestampModeChanged;
}

void toggleDots(bool turnOn) {
  digitalWrite(PIN_DOTS, turnOn ? LOW : HIGH);
}

void updateDisplay() {
  DateTime currentTime = watchCore.now();
  bool isSecondEven = (currentTime.second() % 2 == 0);
  
  display4Digit.setNumber(currentTime.hour() * 100 + currentTime.minute());
  toggleDots(isSecondEven);
}

void handleTimeView() {
  updateDisplay();

  if (btnAlarm.read() == Button::RELEASED && watchCore.alarmActive()) {
    btnAlarm.has_changed();
    switchViewMode(MODE_ALARM_RINGING);
    return;
  }

  if (btnHour.pressed())  watchCore.incrementHour();
  if (btnMin.pressed())   watchCore.incrementMinute();
  
  if (btnAlarm.pressed()) {
    if (!watchCore.alarmEnabled()) {
      watchCore.toggleAlarm();
    }
    switchViewMode(MODE_ALARM_SET);
  }
}

void handleAlarmSetView() {
  bool showDigits = (millis() / 250) % 2 == 0;

  if (showDigits) {
    DateTime alarmSetup = watchCore.alarmTime();
    display4Digit.setNumber(alarmSetup.hour() * 100 + alarmSetup.minute(), -1);
  } else {
    display4Digit.setChars("    ");
  
  toggleDots(false);


  if (getDurationInCurrentMode() > ALARM_HOUR_DISPLAY_TIME) {
    switchViewMode(MODE_SHOW_TIME);
    return;
  }

  if (btnHour.pressed()) {
    watchCore.incrementAlarmHour();
    timestampModeChanged = millis();
  }
  if (btnMin.pressed()) {
    watchCore.incrementAlarmMinute();
    timestampModeChanged = millis();
  }

  if (btnAlarm.pressed()) {
    switchViewMode(MODE_SHOW_TIME);
  }
}
}
void handleRingingView() {
  updateDisplay();

  if (btnAlarm.read() == Button::RELEASED) {
    soundModule.play();
  }
  if (btnAlarm.pressed()) {
    soundModule.stop();
  }
  if (btnAlarm.released()) {
    soundModule.stop();
    

    if (btnAlarm.repeat_count() > 0) {
      watchCore.stopAlarm();
      switchViewMode(MODE_SHOW_TIME);
    } else {
      watchCore.snooze();
      switchViewMode(MODE_SNOOZE_CONFIRM);
    }
  }
}

void handleSnoozeView() {
  display4Digit.setChars("****");
  
  if (getDurationInCurrentMode() > SNOOZE_DISPLAY_TIME) {
    switchViewMode(MODE_SHOW_TIME);
    return;
  }
}