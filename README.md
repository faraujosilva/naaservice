Open Network Orchestration Tool (Prototipo para fins de estudo)
=======
ONOT é uma ferrementa de automação focada na automação de elementos de redes de diversos fabricantes, versões e formas de acesso.
Como um complemento para todo ecossistema de automação existente hoje, o ONOT consegue interagir com scripts em python, playbooks em ansible, comandos SNMP de GET, RestConf/NetConf, SSH, Telnet e RESTAPI, formatando e garantindo uma comunicação a nível corporativo com o ambiente de Rede através da exposição de APIs, com o principal objetivo de unificar, centralizar e padronizar todas ferramentas e maneiras que temos de lidar com automação em um único lugar, independente da sua escolha de connector(seja netmiko, e etc.).

A base da arquitetura é no NSO (Cisco Network Services Orchestrator) com um diferencial de proporcionar maior flexbilidade para que os NEDs( NSO ) sejam qualquer coisa, desde um playbook até um simples SNMP, removendo a complexidade de definir modelos YANG.


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
   * Os drivers(SSH e etc) interagem com os connectors(implementações do SSH, como Netmiko etc) para alcançar os elementos.
   * Se o driver prioritário padrão não for definido, então uma ordem default será executada (consultar DriverOrder class), e isso também serve caso o driver prioritário falhe, a ordem de 'fallback' é respeitada.
Architecture
=================
![Logo](docs/imgs/architecture.png)
  

Use Cases
============
   * Monitoria inteligente com Zabbix e demais ferramentas.
   * Validar uniformemente se uma configuração existe em um grupo de equipamentos.
   * Disponibilizar APIs de serviços para integrações com ferramentas de ITSM como o ServiceNow para reservas automaticas de IP, interfaces, criação de novas VLANs e automaizações de deployments em ambientes de NGN(ACI, DNA, etc).
   * Integração da pipeline da empresa com o ambiente de rede para validações de testes de conectividade.
   * Integração de qualquer ferrramenta com o ambiente de rede via API seguindo as boas práticas.
   * Armazenar o estado da coleta de vários comandos afim de garantir um historíco linear do comportamento da rede.
   * Automatizar vários comandos em diversos equipamentos de vendors e versõse diferentes com apenas um JSON, como por exemplo validações antes e após mudanças no ambiente.

   * Para detalhes da implementação consulte:
      - [Exemplos de API](docs/examples/API.md)
      - [Exemplos de CLI](docs/examples/CLI.md)





RoadMap
=======
   * Implementar conectors para RestConf/NetConf, Snippets e ansible
   * Armazenamento de estados e configurações no banco
   * Features de aplicar configurações com estados e rollbacks
   * Expandir solução para outros vendors e outros comandos
   * Pipeline CI
   * Testes
   * PyAts e Genie
   * Simplificar JSON
   * Filtros nas requisições (qual campo do output retornar/pesquisar com operadores HTTP)
   * Auto detect para device types ( router, switch etc )
   * Integração com CMDBs/DCIMs/ITSM tools

Authors
=======
Criado por [Fernando](https://github.com/faraujosilva)

