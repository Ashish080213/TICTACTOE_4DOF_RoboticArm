#include <Servo.h>

int pos = 0;

Servo arm1servo;
Servo arm2servo;
Servo baseservo;
Servo gripservo;

int ang = 60;
int cang = 0;
double x;
double y;
double z;

int baseangle2 = 130;
int baseangle = 45;
int elbowangle = 60;
int handangle = 120;
int gripAngle = 0;

void setup() {
  baseservo.attach(11);
  gripservo.attach(8);
  arm2servo.attach(7);
  arm1servo.attach(5);
  baseservo.write(baseangle2);
  // delay(2000);
  gripservo.write(gripAngle);
  // delay(2000);
  arm2servo.write(handangle);
  // delay(2000);
  arm1servo.write(elbowangle);
  // delay(2000);
  Serial.begin(9600);
  Serial.setTimeout(10);
  delay(5000);
}

void sgrip(int cang, int ang) {
  if (ang > cang) {
    for (int pos = cang; pos < ang; pos += 1) {
      gripservo.write(pos);
      delay(15);
    }
  } else if (ang < cang) {
    for (int pos = cang; pos > ang; pos -= 1) {
      gripservo.write(pos);
      delay(15);
    }
  }
}

void sbase(int cang, int ang) {
  if (ang > cang) {
    for (int pos = cang; pos < ang; pos += 1) {
      baseservo.write(pos);
      delay(15);
    }
  }

  else if (ang < cang) {
    for (int pos = cang; pos > ang; pos -= 1) {
      baseservo.write(pos);
      delay(15);
    }
  }
}

void sarm1(int cang, int ang) {
  if (ang > cang) {
    for (int pos = cang; pos < ang; pos += 1) {
      arm1servo.write(pos);
      delay(15);
    }
  }

  else if (ang < cang) {
    for (int pos = cang; pos > ang; pos -= 1) {
      arm1servo.write(pos);
      delay(15);
    }
  }
}
void sarm2(int cang, int ang) {
  if (ang > cang) {
    for (int pos = cang; pos < ang; pos += 1) {
      arm2servo.write(pos);
      delay(15);
    }
  }

  else if (ang < cang) {
    for (int pos = cang; pos > ang; pos -= 1) {
      arm2servo.write(pos);
      delay(15);
    }
  }
}

void moveToAngle(double b, double a1, double a2, double g) {
  sbase(baseangle, (45 - b / 1.2));
  Serial.println("BASE");
  Serial.println(b);
  delay(3000);
  sarm1(elbowangle, (200 - a1));
  Serial.println("ELBOW");
  Serial.println(a1);
  delay(3000);
  sarm2(handangle, 120 + a2 - 30);
  Serial.println("HAND");
  Serial.println(120 + a2);
  delay(3000);
  sgrip(gripAngle, (g + 60));
  Serial.println("GRIPPER");
  Serial.println(g + 60);
  delay(3000);

  for (int pos = 120 + a2 - 30; pos < handangle; pos += 1) {
    arm2servo.write(pos);
    delay(15);
  }
  delay(2000);

  for (int pos = 200 - a1; pos > elbowangle; pos -= 1) {
    arm1servo.write(pos);
    delay(15);
  }
  delay(2000);

  if (45 - b / 1.2 < 45) {
    for (int pos = 45 - b / 1.2; pos < baseangle; pos += 1) {
      baseservo.write(pos);
      delay(15);
    }
    delay(2000);
  } else {
    for (int pos = 45 - b / 1.2; pos > baseangle; pos -= 1) {
      baseservo.write(pos);
      delay(15);
    }
    delay(2000);
  }
  gripservo.write(gripAngle);
  delay(2000);

  for (int pos = 45; pos < baseangle2; pos += 1) {
    baseservo.write(pos);
    delay(15);
  }
  delay(2000);
}

void moveToPos(double x, double y, double z, double g) {
  double b = atan2(x, y) * (180 / 3.1415);

  double l = sqrt(x * x + y * y);

  double h = sqrt(l * l + z * z);

  Serial.println(h);
  delay(1000);

  double phi = atan(z / l) * (180 / 3.1415);

  double theta = acos((h / 2) / 90) * (180 / 3.1415);

  double a1 = phi + theta;
  double a2 = phi - theta;
  Serial.println(a1);
  delay(1000);
  Serial.println(a2);
  delay(1000);
  Serial.println(b);
  delay(1000);
  Serial.println(g);
  delay(1000);
  moveToAngle(b, a1, a2, g);
}

void loop() {

  if (Serial.available() > 0) {
    String msg = Serial.readString();
    if (msg == "1") {
      x = -55;
      y = 106;
      z = 40;
    } else if (msg == "2") {
      x = 0;
      y = 106;
      z = 40;
    } else if (msg == "3") {
      x = 55;
      y = 106;
      z = 40;
    } else if (msg == "4") {
      x = -55;
      y = 63;
      z = 40;
    } else if (msg == "5") {
      x = 0;
      y = 63;
      z = 40;
    } else if (msg == "6") {
      x = 55;
      y = 63;
      z = 40;
    } else if (msg == "7") {
      x = -55;
      y = 21;
      z = 40;
    } else if (msg == "8") {
      x = 0;
      y = 21;
      z = 40;
    } else if (msg == "9") {
      x = 55;
      y = 21;
      z = 40;
    }

    for (int pos = gripAngle; pos < 60; pos += 1) {
      gripservo.write(pos);
      delay(15);
    }

    delay(2000);

    for (int pos = elbowangle; pos < 80; pos += 1) {
      arm1servo.write(pos);
      delay(15);
    }

    delay(3000);

    for (int pos = 60; pos > gripAngle; pos -= 1) {
      gripservo.write(pos);
      delay(15);
    }

    delay(1000);

    for (int pos = 80; pos > elbowangle; pos -= 1) {
      arm1servo.write(pos);
      delay(15);
    }

    delay(2000);

    for (int pos = 130; pos > baseangle; pos -= 1) {
      baseservo.write(pos);
      delay(15);
    }

    // Serial.println("x");  // Testing only
    // while (Serial.available() == 0) {
    //   // Wait for user input
    // }
    // x = Serial.parseFloat();
    // Serial.println(x);

    // Serial.flush();

    // Serial.println("y");
    // while (Serial.available() == 0) {
    //   // Wait for user input
    // }
    // y = Serial.parseFloat();
    // Serial.println(y);

    // Serial.println("z");
    // while (Serial.available() == 0) {
    //   // Wait for user input
    // }
    // z = Serial.parseFloat();
    // Serial.println(z);
    delay(2000);

    // for (pos = 0; pos <= ang; pos += 1) {
    //   gripservo.write(pos);
    //   delay(15);
    // }
    // for (pos = ang; pos >= 0; pos -= 1) {
    //   gripservo.write(pos);
    //   delay(15);
    // }

    moveToPos(x, y, z, gripAngle);
  }
}
