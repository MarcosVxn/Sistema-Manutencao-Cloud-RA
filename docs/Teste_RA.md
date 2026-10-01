# Matriz de Testes

Este documento apresenta os testes realizados no protótipo do Sistema de Apoio à Manutenção Industrial com Realidade Aumentada e Serviços em Nuvem.

Os testes têm como objetivo verificar o funcionamento da aplicação WebAR, integração com a API Flask, comunicação MQTT e tratamento de indisponibilidade.

---

## T01 — Abertura da WebAR

**Ação:**  
Abrir a aplicação WebAR em um dispositivo móvel compatível.

**Resultado esperado:**  
A aplicação deve carregar corretamente e solicitar/acessar a câmera do dispositivo.

**Resultado obtido:**  
A aplicação carregou corretamente e a câmera ficou disponível.

**Status:** ✅ Aprovado

---

## T02 — Reconhecimento do Target

**Ação:**  
Apontar a câmera do dispositivo para o target associado ao equipamento.

**Resultado esperado:**  
O sistema deve reconhecer o target e ativar a experiência de Realidade Aumentada.

**Resultado obtido:**  
O target foi reconhecido e a experiência de RA foi ativada.

**Status:** ✅ Aprovado

---

## T03 — Tracking do Target

**Ação:**  
Movimentar o celular mantendo o target dentro do campo de visão da câmera.

**Resultado esperado:**  
Os hotspots devem acompanhar a posição do equipamento durante o tracking.

**Resultado obtido:**  
Os hotspots acompanharam o target durante a movimentação do dispositivo.

**Status:** ✅ Aprovado

---

## T04 — Hotspot Técnico

**Ação:**  
Tocar em um hotspot responsável por apresentar informações técnicas do equipamento.

**Resultado esperado:**  
O sistema deve apresentar as informações estáticas relacionadas ao equipamento ou componente selecionado.

**Resultado obtido:**  
As informações técnicas foram apresentadas corretamente.

**Status:** ✅ Aprovado

---

## T05 — Consulta de Monitoramento

**Ação:**  
Tocar no hotspot de monitoramento.

**Resultado esperado:**  
A aplicação deve realizar uma requisição HTTP para a API Flask, receber os dados em formato JSON e apresentar as informações na interface de RA.

**Resultado obtido:**  
A API foi consultada e os dados de monitoramento foram apresentados na aplicação.

**Status:** ✅ Aprovado

---

## T06 — Atualização via MQTT

**Ação:**  
Publicar um novo valor de telemetria por meio do broker MQTT.

**Resultado esperado:**  
O serviço responsável deve receber a mensagem MQTT e atualizar o dado de telemetria armazenado.

**Resultado obtido:**  
O novo valor foi recebido pelo serviço e atualizado corretamente.

**Status:** ✅ Aprovado

---

## T07 — Consulta do Novo Valor

**Ação:**  
Realizar uma nova consulta de monitoramento pela aplicação WebAR após a atualização via MQTT.

**Resultado esperado:**  
A aplicação deve apresentar o novo valor recebido pelo serviço.

**Resultado obtido:**  
O novo valor de telemetria foi apresentado corretamente na aplicação.

**Status:** ✅ Aprovado

---

## T08 — Indisponibilidade da API

**Ação:**  
Interromper temporariamente o serviço da API Flask e tentar consultar os dados de monitoramento pela WebAR.

**Resultado esperado:**  
A aplicação deve permanecer funcional e apresentar uma mensagem informando que não foi possível consultar os dados do equipamento.

**Resultado obtido:**  
A aplicação permaneceu acessível e apresentou uma mensagem de indisponibilidade da API.

**Status:** ✅ Aprovado

---

## T09 — Restauração da API

**Ação:**  
Restaurar o serviço da API Flask e realizar novamente a consulta de monitoramento.

**Resultado esperado:**  
A aplicação deve voltar a consultar a API normalmente e apresentar os dados do equipamento.

**Resultado obtido:**  
A consulta voltou a funcionar após a restauração da API.

**Status:** ✅ Aprovado

---

## Resumo dos Testes

| ID | Teste | Resultado |
|---|---|---|
| T01 | Abrir WebAR | ✅ Aprovado |
| T02 | Reconhecer Target | ✅ Aprovado |
| T03 | Tracking do Target | ✅ Aprovado |
| T04 | Tocar no hotspot técnico | ✅ Aprovado |
| T05 | Consultar monitoramento pela API | ✅ Aprovado |
| T06 | Publicar novo valor via MQTT | ✅ Aprovado |
| T07 | Consultar novo valor na WebAR | ✅ Aprovado |
| T08 | Interromper a API | ✅ Aprovado |
| T09 | Restaurar a API | ✅ Aprovado |

---

## Conclusão

Os testes verificam o fluxo principal da solução, desde o reconhecimento do equipamento pela aplicação WebAR até a consulta de dados dinâmicos provenientes da API e a atualização dos dados por meio do MQTT.

Também foi verificado o comportamento da aplicação durante a indisponibilidade da API, garantindo que o usuário receba uma mensagem compreensível em caso de falha do serviço.