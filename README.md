# RPG de Texto em Python

Um jogo de RPG no terminal feito em Python. Foi o meu primeiro projeto de programação, construído por etapas para aprender na prática.

Você cria um herói e enfrenta três monstros em sequência: Goblin, Orc e Dragão. A cada vitória ganha XP e pode subir de nível.

## O que o jogo tem

- Batalhas por turnos (atacar, usar poção ou fugir)
- Dano aleatório a cada golpe
- Inventário com poções que recuperam vida
- Sistema de XP e níveis (mais dano e mais vida ao subir de nível)
- Chance de 40% de fugir da batalha
- Salvamento automático depois de cada vitória, com a opção de continuar a aventura

## Como rodar

É preciso ter o [Python 3](https://www.python.org/downloads/) instalado.

```
python rpg.py
```

No menu, escolha `1` para um novo jogo ou `2` para continuar de onde parou. O progresso fica no arquivo `save.json`, criado na mesma pasta.

## O que eu pratiquei

- Variáveis, listas e dicionários
- Condicionais (`if`, `elif`, `else`) e laços (`while`, `for`)
- Funções e variáveis globais
- Números aleatórios com o módulo `random`
- Leitura e escrita de arquivos JSON

## Ideias para o futuro

- Mais monstros e itens
- Loja para comprar poções
- Classes de herói (guerreiro, mago)
