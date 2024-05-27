# Sistema de Registros de Entrada/Saída

Este projeto é uma aplicação web desenvolvida em Flask para registrar e listar movimentações de entrada e saída de carros em estacionamentos utilizando o Firebase Firestore como banco de dados.

## Descrição

A aplicação permite registrar movimentações de entrada e saída de carros em estacionamentos, armazenando essas informações no Firebase Firestore. Além disso, fornece uma interface web para visualizar as entradas e saídas registradas.

## Uso

### Registrar uma Movimentação

Para registrar uma movimentação de entrada ou saída, envie uma requisição POST para o endpoint `/registro` com o seguinte payload JSON:

```json
{
    "tipo": "Entrada"
}
