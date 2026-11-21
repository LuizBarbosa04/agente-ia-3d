
# Agente de IA para Modelagem e Impressão 3D

Projeto de desenvolvimento de um agente de inteligência artificial local capaz de interpretar solicitações em linguagem natural, validar parâmetros geométricos e automatizar a criação de modelos CAD para impressão 3D.

## Objetivo

Desenvolver um sistema que integre inteligência artificial, programação Python e modelagem paramétrica para facilitar a criação de peças personalizadas.

O projeto utiliza modelos de linguagem executados localmente, sem depender de APIs comerciais para interpretar solicitações.

## Tecnologias

- Python 3.12
- Ollama
- Qwen3:4b
- Pydantic
- FreeCAD 1.1
- Creality Print
- Git e GitHub

## Funcionamento

1. O usuário descreve a peça em linguagem natural.
2. O Qwen interpreta a solicitação e extrai parâmetros estruturados.
3. O agente identifica e solicita informações ausentes.
4. O Pydantic valida os parâmetros geométricos.
5. O usuário confirma as dimensões.
6. O Python executa a automação CAD no FreeCAD.
7. O sistema gera arquivos FCStd e STL.

## Funcionalidades implementadas

- Integração local com Ollama e Qwen.
- Interpretação de solicitações em português.
- Extração estruturada de parâmetros.
- Identificação de dimensões ausentes.
- Validação geométrica com Pydantic.
- Confirmação antes da geração.
- Criação automatizada de caixas retangulares.
- Exportação de arquivos FCStd e STL.
- Preservação de versões anteriores.

## Limitações atuais

Nesta fase, o agente gera apenas caixas retangulares abertas na parte superior, com fundo fechado e sem tampa.

A organização automática de cada geração em uma pasta própria está em desenvolvimento.

## Estrutura do projeto

```text
agente-3d/
├── cad/
│   └── gerar_caixa.py
├── agente_3d.py
├── executar_cad.py
├── gerenciador_projetos.py
├── models.py
├── parametros_caixa.json
├── teste_interpretacao.py
├── teste_ollama.py
├── teste_validacao.py
├── .gitignore
└── README.md
```

## Requisitos

- Windows
- Python 3.12
- Ollama com o modelo qwen3:4b
- FreeCAD 1.1
- Bibliotecas Python: ollama e pydantic

## Execução

Com o ambiente virtual ativado e as dependências instaladas:

```powershell
ollama pull qwen3:4b
python agente_3d.py
```

O Ollama deve estar em execução e o caminho do FreeCADCmd deve estar configurado no arquivo `executar_cad.py`.

## Próximas funcionalidades

- Organização automática dos projetos gerados.
- Histórico de modelos e versões.
- Suporte a novas geometrias.
- Geração de peças com furos e encaixes.
- Aprimoramento das validações.
- Integração com o fluxo de fatiamento para impressão 3D.

## Status

Em desenvolvimento — MVP funcional para geração automatizada de caixas retangulares.
