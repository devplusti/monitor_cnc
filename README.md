# monitor_cnc
Quando os sensores da máquina indicar que uma peça foi produzida, ele aumenta o contador e envia os dados para um arquivo de texto (futuramente para a base de dados).

O programa também gerencia abertura e encerramento de ordens de produção, operações de setup e solicita códigos de paradas.

**Componentes:**
- display LCD 2 linhas (I2C_LCD_driver)
- Teclado Matricial Membrana (pad4pi)
