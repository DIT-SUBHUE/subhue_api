# Módulo Subhue API

Este módulo fornece uma interface para integração com a API Subhue, seguindo os princípios SOLID de design de software.

## Estrutura do Módulo

O módulo foi refatorado para seguir uma arquitetura mais modular e manutenível:

```
modules/apis/subhue/
├── __init__.py        - Exporta a classe principal
├── auth.py            - Classes de autenticação
├── client.py          - Cliente HTTP e processamento de respostas
├── config.py          - Configuração de endpoints
├── converters.py      - Conversão de tipos de dados
├── endpoints.py       - Definição centralizada de URLs
├── processors.py      - Processamento de dados e envio em lotes
└── subhue.py          - Classe principal (fachada)
```

## Princípios SOLID Aplicados

1. **Princípio da Responsabilidade Única (SRP)**
   - Cada classe tem uma única responsabilidade
   - Ex: `DataConverter`, `TokenAuth`, `ApiClient`, etc.

2. **Princípio Aberto/Fechado (OCP)**
   - As classes estão abertas para extensão, fechadas para modificação
   - Ex: Novas formas de autenticação podem ser adicionadas implementando `ApiAuth`

3. **Princípio da Substituição de Liskov (LSP)**
   - As implementações respeitam os contratos de suas interfaces
   - Ex: `HttpClient` implementa corretamente `ApiClient`

4. **Princípio da Segregação de Interface (ISP)**
   - Interfaces pequenas e específicas em vez de uma grande interface
   - Ex: `ApiAuth` e `ApiClient` são interfaces focadas

5. **Princípio da Inversão de Dependência (DIP)**
   - Dependência de abstrações, não de implementações concretas
   - Ex: `BatchProcessor` depende de `ApiClient`, não de `HttpClient`

## Como Usar

### Uso Básico

```python
from vitai.modules.apis import Subhue

# Usar o ambiente de produção (padrão)
api = Subhue(endpoint="altas")

# Ou usar um ambiente específico
api_dev = Subhue(endpoint="altas", environment="dev")
api_local = Subhue(endpoint="altas", environment="local")

# Preparar dados de um DataFrame
df = pd.DataFrame(...)
payload = api.prepare_payload_from_dataframe(
    df,
    date_columns=["data_alta"],
    numeric_columns=["idade"]
)

# Enviar dados
api.send_payload(payload, batch_size=10, sleep_time=1)
```

### Ambientes Disponíveis

- `prod`: Produção (padrão) - https://api.subhue.org
- `dev`: Desenvolvimento - https://api-dev.subhue.org
- `local`: Desenvolvimento local - http://127.0.0.1:8000

### Endpoints Disponíveis

- `altas`: Altas de pacientes
- `atendimentos`: Atendimentos
- `atendimentos_update`: Atualização de atendimentos
- `censo_leitos`: Censo de leitos
- `los`: Length of Stay (Permanência)
- `ociosidade`: Ociosidade de leitos
- `classificados`: Classificados
- `registrados`: Registrados
- `unidades`: Unidades
- `auth`: Autenticação

## Configuração

As URLs dos endpoints estão definidas diretamente no código, no arquivo `endpoints.py`, sem necessidade de variáveis de ambiente.