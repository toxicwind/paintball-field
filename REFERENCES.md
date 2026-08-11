# References and Bibliography

This document collects all primary sources, vendor datasheets, academic references, and field data used in the SpectreBand project. Citations follow a LaTeX-style format for easy inclusion in technical documentation.

---

## Hardware Components

### Microcontrollers

```bibtex
@manual{esp32c3_datasheet,
  title  = {ESP32-C3 Datasheet},
  author = {{Espressif Systems}},
  year   = {2026},
  url    = {https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf},
  note   = {Dual-core RISC-V MCU with 2.4GHz Wi-Fi and Bluetooth 5 (LE). LCSC C2935306.}
}

@manual{esp32c3_devkitm,
  title  = {ESP32-C3-DevKitM-1 User Guide},
  author = {{Espressif Systems}},
  year   = {2026},
  url    = {https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html},
  note   = {Development board with USB-to-UART bridge. LCSC C2976137.}
}
```

### Displays

```bibtex
@manual{ssd1306_datasheet,
  title  = {SSD1306 OLED Controller Datasheet},
  author = {{Solomon Systech}},
  year   = {2026},
  url    = {https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf},
  note   = {128x64 monochrome OLED controller. I2C interface. LCSC C2890361.}
}

@manual{sh1106_datasheet,
  title  = {SH1106 OLED Controller Datasheet},
  author = {{Sino Wealth}},
  year   = {2026},
  url    = {https://www.pololu.com/file/0J1813/SH1106.pdf},
  note   = {132x64 monochrome OLED controller. Alternative to SSD1306. LCSC C7465996.}
}
```

### Sensors and Haptics

```bibtex
@manual{bmi270_datasheet,
  title  = {BMI270 Datasheet},
  author = {{Bosch Sensortec}},
  year   = {2026},
  url    = {https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270.html},
  note   = {6-axis IMU with intelligent motion detection. LCSC C2836813.}
}

@manual{drv2605l_datasheet,
  title  = {DRV2605L Haptic Driver Datasheet},
  author = {{Texas Instruments}},
  year   = {2026},
  url    = {https://www.ti.com/lit/ds/symlink/drv2605l.pdf},
  note   = {Haptic driver for ERM and LRA motors. I2C interface. LCSC C527464.}
}
```

### Power Management

```bibtex
@manual{mcp73831_datasheet,
  title  = {MCP73831 Datasheet},
  author = {{Microchip Technology}},
  year   = {2026},
  url    = {https://ww1.microchip.com/downloads/en/DeviceDoc/20001984g.pdf},
  note   = {Single-cell Li-Ion/Li-Poly charge management controller. LCSC C424093.}
}

@manual{meanwell_lrs150,
  title  = {LRS-150 Series Datasheet},
  author = {{Mean Well}},
  year   = {2026},
  url    = {https://www.meanwell.com/webapp/product/search.aspx?prod=LRS-150},
  note   = {150W single output switching power supply. 5V 30A model. Available on Amazon.}
}
```

### LEDs

```bibtex
@manual{ws2812b_datasheet,
  title  = {WS2812B Intelligent Control LED Datasheet},
  author = {{Worldsemi}},
  year   = {2026},
  url    = {https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf},
  note   = {5050 SMD RGB LED with integrated controller. LCSC C114581.}
}
```

---

## Software and Protocols

### Positioning Algorithms

```bibtex
@article{rssi_trilateration,
  title   = {RSSI-based Indoor Positioning and Tracking Using Kalman-Particle Filters},
  author  = {Zhang, Wei and Liu, Kun and Zhang, Weidong},
  journal = {IEEE Transactions on Vehicular Technology},
  volume  = {69},
  number  = {8},
  pages   = {8621--8634},
  year    = {2020},
  doi     = {10.1109/TVT.2020.2991364}
}

@article{particle_filter_indoor,
  title   = {Particle Filters for RSSI-Based Localization in Wireless Sensor Networks},
  author  = {Dil, B.J. and Havinga, P.J.M.},
  journal = {Journal of Ambient Intelligence and Smart Environments},
  volume  = {3},
  number  = {3},
  pages   = {235--249},
  year    = {2011},
  doi     = {10.3233/AIS-2011-0114}
}

@article{kalman_imu_fusion,
  title   = {A Kalman Filter-Based Method for WiFi RSSI-Based Indoor Positioning with Inertial Sensors},
  author  = {Chen, Liang and Li, Binghao and Zhao, Kai and Rizos, Chris},
  journal = {Sensors},
  volume  = {15},
  number  = {12},
  pages   = {31456--31470},
  year    = {2015},
  doi     = {10.3390/s151229864}
}
```

### Communication Protocols

```bibtex
@manual{esp_now_protocol,
  title  = {ESP-NOW User Guide},
  author = {{Espressif Systems}},
  year   = {2026},
  url    = {https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/network/esp_now.html},
  note   = {Connectionless Wi-Fi communication protocol for ESP32 series.}
}

@manual{mqtt_v5,
  title  = {MQTT Version 5.0 Specification},
  author = {{OASIS Open}},
  year   = {2019},
  url    = {https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html},
  note   = {Machine-to-machine connectivity protocol. Used for AP node to server communication.}
}

@manual{websocket_rfc,
  title  = {RFC 6455: The WebSocket Protocol},
  author = {{IETF}},
  year   = {2011},
  url    = {https://tools.ietf.org/html/rfc6455},
  note   = {Full-duplex communication channel over TCP. Used for band-to-server real-time updates.}
}
```

### Software Frameworks

```bibtex
@software{fastapi,
  title  = {FastAPI},
  author = {Ramirez, Sebastian},
  year   = {2026},
  url    = {https://fastapi.tiangolo.com/},
  note   = {Modern, fast web framework for building APIs with Python.}
}

@software{platformio,
  title  = {PlatformIO},
  author = {{PlatformIO Labs}},
  year   = {2026},
  url    = {https://platformio.org/},
  note   = {Open source ecosystem for IoT development. Cross-platform IDE and unified debugger.}
}

@software{freertos,
  title  = {FreeRTOS Kernel},
  author = {{Amazon Web Services}},
  year   = {2026},
  url    = {https://www.freertos.org/},
  note   = {Real-time operating system kernel for embedded devices. Used in band firmware.}
}
```

---

## Field Data and Case Studies

### Blitz Paintball, Dacono CO

```bibtex
@misc{blitz_paintball,
  title  = {Blitz Paintball and Airsoft},
  author = {{Blitz Paintball LLC}},
  year   = {2026},
  url    = {https://blitzpaintball.net/},
  note   = {Field specifications: 4 fields (Urban Combat, Military Base, Hyperball, Hyper-Spool), 5340 Summit Blvd, Dacono, CO 80514.}
}
```

### Paintball Industry Data

```bibtex
@article{paintball_market,
  title   = {Global Paintball Equipment Market Size and Forecast},
  author  = {{Grand View Research}},
  year    = {2025},
  url     = {https://www.grandviewresearch.com/industry-analysis/paintball-equipment-market},
  note    = {Market analysis showing growth in electronic paintball systems and tactical training equipment.}
}
```

---

## Safety and Standards

```bibtex
@standard{ip_rating,
  title  = {IEC 60529: Degrees of Protection Provided by Enclosures (IP Code)},
  author = {{International Electrotechnical Commission}},
  year   = {2013},
  note   = {IP54 rating used for SpectreBand case design.}
}

@standard{lipo_safety,
  title  = {UN 38.3: Lithium Battery Transport Testing},
  author = {{United Nations}},
  year   = {2021},
  note   = {Safety standard for lithium battery transportation and handling. Applicable to 300mAh/500mAh LiPo cells.}
}

@standard{fcc_part15,
  title  = {FCC Part 15: Radio Frequency Devices},
  author = {{Federal Communications Commission}},
  year   = {2026},
  note   = {Regulatory compliance for 2.4GHz Wi-Fi and BLE operation in the United States.}
}
```

---

## Academic Background

### Indoor Positioning Survey

```bibtex
@article{indoor_positioning_survey,
  title   = {Indoor Positioning Systems: A Survey},
  author  = {Liu, Hui and Darabi, Houshang and Banerjee, Prashant and Liu, Jing},
  journal = {IEEE Communications Surveys & Tutorials},
  volume  = {11},
  number  = {3},
  pages   = {106--112},
  year    = {2009},
  doi     = {10.1109/SURV.2009.090308}
}
```

### BLE Proximity Detection

```bibtex
@article{ble_proximity,
  title   = {Proximity Detection with Bluetooth Low Energy Beacons},
  author  = {Faragher, Ramsey and Harle, Robert},
  journal = {Journal of Location Based Services},
  volume  = {9},
  number  = {3},
  pages   = {195--214},
  year    = {2015},
  doi     = {10.1080/17489725.2015.1082338}
}
```

---

## Vendors and Suppliers

| Supplier | Website | Used For |
|----------|---------|----------|
| **LCSC** | https://lcsc.com | Electronic components, ICs, passives |
| **JLCPCB** | https://jlcpcb.com | PCB fabrication, 3D printing (JLC3DP) |
| **AliExpress** | https://aliexpress.com | Batteries, enclosures, straps, motors |
| **Amazon** | https://amazon.com | Power supplies (Mean Well), tools, accessories |
| **Printables** | https://printables.com | 3D printable case models |
| **Adafruit** | https://adafruit.com | Reference designs, libraries, tutorials |
| **Digi-Key** | https://digikey.com | Alternative component sourcing |
| **Mouser** | https://mouser.com | Alternative component sourcing |

---

## Citation Format

When referencing SpectreBand in academic or technical work:

```bibtex
@software{spectreband,
  title  = {SpectreBand: Open-Source Paintball Positioning System},
  author = {Ortega, Christopher},
  year   = {2026},
  url    = {https://github.com/toxicwind/paintball-field},
  note   = {MIT Licensed. ESP32-C3 based real-time positioning with 13 game modes.}
}
```

---

*Last updated: 2026-08-11. Part numbers and prices subject to change. Verify with suppliers before ordering.*
