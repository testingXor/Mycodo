Mycodo é um sistema de monitorização e regulação ambiental de código aberto que foi construído para funcionar em computadores de placa única, especificamente o [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi).

Originalmente desenvolvido para o cultivo de cogumelos comestíveis, Mycodo tem crescido para fazer muito mais. O sistema consiste em duas partes, um backend (daemon) e um frontend (servidor web). O backend executa tarefas tais como adquirir medições de sensores e dispositivos e coordenar um conjunto diversificado de respostas a essas medições, incluindo a capacidade de modular saídas (comutar relés, gerar sinais PWM, operar bombas, mudar saídas sem fios, publicar/assinar ao MQTT, entre outros), regular as condições ambientais com controlo PID, programar temporizadores, capturar fotos e transmitir vídeo, desencadear acções quando as medições satisfazem determinadas condições, e muito mais. O frontend aloja uma interface web que permite a visualização e configuração a partir de qualquer dispositivo activado por browser.

Existem várias utilizações diferentes para Mycodo. Alguns utilizadores simplesmente armazenam medições de sensores para monitorizar as condições à distância, outros regulam as condições ambientais de um espaço físico, enquanto outros captam fotografia activada por movimento ou time-lapse, entre outras utilizações.

Os controladores de entrada adquirem medidas e armazenam-nas na base de dados de séries temporais InfluxDB. As medições vêm tipicamente de sensores, mas também podem ser configuradas para utilizar o valor de retorno dos comandos Linux Bash ou Python, ou equações matemáticas, tornando-o um sistema muito dinâmico para a aquisição e geração de dados.

Os controladores de saída produzem alterações nos pinos de entrada/saída geral (GPIO) ou podem ser configurados para executar comandos Linux Bash ou Python, permitindo uma variedade de usos potenciais. Existem alguns tipos diferentes de saídas: simples comutação de pinos GPIO (HIGH/LOW), geração de sinais de largura de pulso modulada (PWM), controlo de bombas peristálticas, publicação de MQTT, e muito mais.

Quando as Entradas e Saídas são combinadas, os controladores de funções podem ser utilizados para criar laços de feedback que utilizam o dispositivo de Saída para modular uma condição ambiental as medidas de Entrada. Certas Entradas podem ser acopladas a certas Saídas para criar uma variedade de diferentes aplicações de controlo e regulação. Para além da regulação simples, podem ser utilizados métodos para criar um ponto de ajuste variável ao longo do tempo, permitindo coisas como termocicladores, fornos de refluxo, simulação ambiental para terrários, fermentação ou cura de alimentos e bebidas, e cozinhar alimentos ([sous-vide](https://en.wikipedia.org/wiki/Sous-vide)), para citar alguns.

Os gatilhos podem ser definidos para activar eventos com base em datas e horas específicas, de acordo com durações de tempo, ou o nascer/pôr-do-sol a uma latitude e longitude específicas.

Mycodo foi traduzido para várias línguas. Por defeito, o idioma do navegador irá determinar qual o idioma utilizado, mas pode ser anulado nas Configurações Gerais, na página `[Ícone do Equipamento] -> Configurar -> Geral'. Se encontrar um problema e quiser corrigir uma tradução ou quiser acrescentar outra língua, isto pode ser feito em [https://translate.kylegabriel.com](http://translate.kylegabriel.com:8080/engage/mycodo/).