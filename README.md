Open Network Orchestration Tool (Prototipo)
=======
ONOT é uma ferrementa de automação focada na automação de elementos de redes de diversos fabricantes, versões e formas de acesso.
Como um complemento para todo ecossistema de automação existente hoje, o ONOT consegue interagir com scripts em python, playbooks em ansible, comandos SNMP de GET, RestConf/NetConf, SSH, Telnet e RESTAPI, formatando e garantindo uma comunicação a nível corporativo com o ambiente de Rede através da exposição de APIs.


Design
=================

   * Abstrai sintaxes de comandos, padroniza outputs independente da forma de conexão (SSH, SNMP, API e etc) e retorna a informação de forma uniforme via REST API ou CLI.
   * Define os comandos e abstrações em arquivos de configuração JSON, facilitando e otimizando novas integrações.
   * Flexibliidade do meio de conexão, suportando SSH, SNMP, REST, NETCONF e RESTCONF e até snippets de qualquer linguagem.
   * Integra com todo ecossistema relevante na automação de redes até 2024, como netmiko, ansible playbooks, shell e outros, afim de possibilitar a reutilização de scripts existentes.
   * Utiliza regex como forma de parsear e padronizar os outputs das informações incorporadas do arquivo JSON.
   * Não necessário instalar agentes ou ferramentas nos elementos, pois a comunicação acontece com suas formas nativas.
   * Possibilita a expansão para outras formas de API como de configuração, reservas de interface/ip e outros.
   * Auto detecta (se possível) o tipo do driver a ser usado(netmiko) como cisco_ios, nxos e etc.
   * Integra com elementos externos para consumir informações dos elementos como IP, Nome, Vendor e etc como NetBox, CMDBs e outros.

Architecture
=================
![Logo](docs/architecture.png)
  
Use Cases
============
   * Validar uniformemente se uma configuração existe em um grupo de equipamentos.
   * Disponibilizar APIs de serviços para integrações com ferramentas de ITSM como o ServiceNow para reservas automaticas de IP, interfaces, criação de novas VLANs e automaizações de deployments em ambientes de NGN(ACI, DNA, etc).
   * Integração da pipeline da empresa com o ambiente de rede para validações de testes de conectividade.
   * Integração de qualquer ferrramenta com o ambiente de rede via API seguindo as boas práticas.
   * Armazenar o estado da coleta de vários comandos afim de garantir um historíco linear do comportamento da rede.
   * Automatizar vários comandos em diversos equipamentos de vendors e versõse diferentes com apenas um JSON, como por exemplo validações antes e após mudanças no ambiente.

      ```json
      {
         "service_name": "cpu_usage",
         "endpoint": {
            "name": "/cpu_usage",
            "method": "GET",
            "parameters": {
                  "device_ip": {
                     "required": false,
                     "type": "string",
                     "description": "IP address of the device"
                  },
                  "device_name": {
                     "required": false,
                     "type": "string",
                     "description": "Name of the device"
                  },
                  "driver": {
                     "required": false,
                     "type": "string",
                     "description": "Driver to be used to get the CPU usage"
                  }
            }
         },
         "cli": {
            "enabled": true
         },
         "drivers": {
            "ssh": {
                  "netmiko": [
                     {"vendor": "cisco", "os": "ios", "type": "router", "command_name": "cpu_usage", "command": "show processes cpu | include CPU utilization", "parse": "five minutes: (.*)", "group": 1},
                     {"vendor": "cisco", "os": "nxos", "type": "switch", "command_name": "cpu_usage", "command": "show system resources", "parse": "5 minutes:\\s*([0-9.]+)", "group": 1}
                  ],
                  "ansible": [
                     {"vendor": "cisco", "os": "ios", "type": "router", "command_name": "cpu_usage", "command": "./playbooks/cpu_usage_ios.yml", "parse": "five minutes: (.*)", "group": 1},
                     {"vendor": "cisco", "os": "nxos", "type": "router", "command_name": "cpu_usage", "command": "./playbooks/cpu_usage_nxos.yml", "parse": "five minutes: (.*)", "group": 1},
                     {"vendor": "hp", "os": "procurve", "type": "router", "command_name": "cpu_usage", "command": "./playbooks/cpu_usage_hp.yml", "parse": "CPU utilization for five seconds: (.*)", "group": 1}
                  ]
            },
            "snmp": {
                  "pysnmp": [
                     {"vendor": "cisco", "os": "ios", "type": "router", "command_name": "cpu_usage", "command": ".1.3.6.1.4.1.9.2.1.58", "parse": "= (.*)", "group": 1}
                  ]
            },
            "snippet": {
                  "python": [
                     {"vendor": "cisco", "os": "ios", "type": "router", "command_name": "cpu_usage", "command": "./snippets/cpu.py", "parse": "five minutes: (.*)", "group": 1}
                  ],
                  "golang": [
                     {"vendor": "cisco", "os": "ios", "type": "router", "command_name": "cpu_usage", "command": "./snippets/cpu", "parse": "five minutes: (.*)", "group": 1}
                  ]
            },
               "api": {
                  "rest": [
                     {"vendor": "cisco", "os": "viptela", "type": "sdwan", "command_name": "cpu_usage", "command": "device/system/status?deviceId={{device_ip}}", "headers": {"Content-Type": "application/json"}, "field": "data[0].cpu_user", "parse": "(.*)", "group": 1}
                  ],
                  "restconf": [
                     {"vendor": "cisco", "os": "iosxe", "type": "router", "command_name": "cpu_usage", "command": "data/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization/five-seconds", "headers": {"Content-Type": "application/yang-data+json"}, "field": "Cisco-IOS-XE-process-cpu-oper:five-seconds", "parse": "(.*)", "group": 1}
                  ]
               }
            
            }
      }

Authors
=======

Criado por [Fernando](https://github.com/faraujosilva)

