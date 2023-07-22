#include "esp_camera.h"
#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <HardwareSerial.h>

#define MYDEBUG

#define Led_GPIO 33
#define Flash_GPIO 4

#if CONFIG_FREERTOS_UNICORE
#define ARDUINO_RUNNING_CORE 0
#else
#define ARDUINO_RUNNING_CORE 1
#endif

#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

const char *ssid = "wyh";
const char *password = "44444444";
const char *host = "http://192.168.43.169:2020/pic";

#ifdef MYDEBUG
#define RX 14
#define TX 15
WiFiServer server(2233);
HardwareSerial MySerial(2);
void TaskHTTP(void *pvParameters);
void TaskServer(void *pvParameters);
#endif

int CameraInit() {
  //配置摄像头
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;  //摄像头的工作时钟，在允许范围内频率越高帧率就越高

  //----------可用的图像格式----------
  //  PIXFORMAT_RGB565,    // 2BPP/RGB565
  //  PIXFORMAT_YUV422,    // 2BPP/YUV422
  //  PIXFORMAT_GRAYSCALE, // 1BPP/GRAYSCALE
  //  PIXFORMAT_JPEG,      // JPEG/COMPRESSED
  //  PIXFORMAT_RGB888,    // 3BPP/RGB888
  //  PIXFORMAT_RAW,       // RAW
  //  PIXFORMAT_RGB444,    // 3BP2P/RGB444
  //  PIXFORMAT_RGB555,    // 3BP2P/RGB555
  config.pixel_format = PIXFORMAT_JPEG;  //输出JPEG图像

  //----------可用的图像分辨率----------
  //  FRAMESIZE_96x96,    // 96x96
  //  FRAMESIZE_QQVGA,    // 160x120
  //  FRAMESIZE_QQVGA2,   // 128x160
  //  FRAMESIZE_QCIF,     // 176x144
  //  FRAMESIZE_HQVGA,    // 240x176
  //  FRAMESIZE_240x240,  // 240x240
  //  FRAMESIZE_QVGA,     // 320x240
  //  FRAMESIZE_CIF,      // 400x296
  //  FRAMESIZE_VGA,      // 640x480
  //  FRAMESIZE_SVGA,     // 800x600
  //  FRAMESIZE_XGA,      // 1024x768
  //  FRAMESIZE_SXGA,     // 1280x1024
  //  FRAMESIZE_UXGA,     // 1600x1200
  //  FRAMESIZE_QXGA,     // 2048*1536

  config.frame_size = FRAMESIZE_QXGA;  //图像尺寸（640x480）
  config.jpeg_quality = 10;            //（10-63）越小照片质量最好
  config.fb_count = 1;                 //要分配的帧缓冲区数。 如果不止一帧，则将获取每帧（双倍速度）i2s以连续模式运行.仅与JPEG一起使用

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("[ERR]Camera init failed with error 0x%x\n", err);
    return 1;
  }

  sensor_t *s = esp_camera_sensor_get();
  s->set_vflip(s, 1);
  s->set_hmirror(s, 1);

  Serial.println("[INFO]Camera init OK");
  return 0;
}

void WiFiInit(const char *ssid, const char *password) {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("[INFO]WiFi connected");
  Serial.printf("[INFO]LocalIP: %s\n", WiFi.localIP());
}

void setup()
{
  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  pinMode(Led_GPIO, OUTPUT);
  pinMode(Flash_GPIO, OUTPUT);
  WiFiInit(ssid, password);
  CameraInit();

  #ifdef MYDEBUG
  server.begin();
  MySerial.begin(115200, SERIAL_8N1, RX, TX);
  xTaskCreatePinnedToCore(TaskHTTP, "HTTP", 4096, NULL, 1, NULL, ARDUINO_RUNNING_CORE);
  xTaskCreatePinnedToCore(TaskServer, "Server", 4096, NULL, 1, NULL, ARDUINO_RUNNING_CORE);
  #endif
}

void loop() {
#ifndef MYDEBUG
  HTTPClient http;

  int control_state = 0;
  int inByte = 0;
  if (Serial.available() > 0)
  {
    inByte = Serial.read();
    if (inByte == 0x6B)
    {
      control_state = 1;
      // digitalWrite(Flash_GPIO, HIGH);
      // vTaskDelay(50);
      // digitalWrite(Flash_GPIO, LOW);
    }
  }
  if (control_state == 2)
  {
    camera_fb_t *photo = NULL;
    // digitalWrite(Flash_GPIO, HIGH);
    digitalWrite(Led_GPIO, HIGH);
    photo = esp_camera_fb_get();
    digitalWrite(Led_GPIO, LOW);
    // digitalWrite(Flash_GPIO, LOW);
    if (!photo)
    {
      Serial.println("[ERR]Camera take failed");
      return;
    }

    http.begin(host);
    http.addHeader("Content-Type", "image/jpeg");
    int httpCode = http.POST((uint8_t *)photo->buf, photo->len);

    if (httpCode < 0) {
      Serial.printf("[ERR]POST failed, error: %s\n", http.errorToString(httpCode).c_str());
    }
    
    http.end();
    esp_camera_fb_return(photo);
  }
#endif
}

#ifdef MYDEBUG
void TaskHTTP(void *pvParameters)
{
  (void) pvParameters;
  for(;;)
  {
    HTTPClient http;

    int control_state = 0;
    int inByte = 0;
    if (Serial.available() > 0)
    {
      inByte = Serial.read();
      if (inByte == 0x6B)
      {
        control_state = 1;
        // digitalWrite(Flash_GPIO, HIGH);
        // vTaskDelay(50);
        // digitalWrite(Flash_GPIO, LOW);
      }
    }
    if (control_state == 1)
    {
      camera_fb_t *photo = NULL;
      // digitalWrite(Flash_GPIO, HIGH);
      digitalWrite(Led_GPIO, HIGH);
      photo = esp_camera_fb_get();
      digitalWrite(Led_GPIO, LOW);
      // digitalWrite(Flash_GPIO, LOW);
      if (!photo)
      {
        Serial.println("[ERR]Camera take failed");
        #ifdef MYDEBUG
        continue;
        #else
        return;
        #endif
      }

      http.begin(host);
      http.addHeader("Content-Type", "image/jpeg");
      int httpCode = http.POST((uint8_t *)photo->buf, photo->len);

      if (httpCode < 0) {
        Serial.printf("[ERR]POST failed, error: %s\n", http.errorToString(httpCode).c_str());
      }
      
      http.end();
      esp_camera_fb_return(photo);
    }
  }
}

void TaskServer(void *pvParameters)
{
  (void) pvParameters;
  for(;;)
  {
    WiFiClient client = server.available();
    if (client)
    {
      Serial.println("[INFO]Connect");
      while (client.connected())
      {
        if (client.available())
        {
          String readBuff = client.readString();
          MySerial.print(readBuff);
        }
      }
    }
  }
}
#endif