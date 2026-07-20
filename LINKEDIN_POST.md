# Post do LinkedIn — 3 parágrafos + tópicos, EN + PT

---

## 🇧🇷 Português

🛠️ Passei um tempo aprendendo como se avalia a qualidade de agentes de IA — e resolvi construir um exemplo do zero pra fixar o aprendizado.

Modelos de IA que executam tarefas (os "agentes") precisam ser testados em desafios controlados. Mas tem um detalhe que poucos comentam: um teste mal construído dá resultado enganoso — pode aprovar um agente que não resolveu nada, ou reprovar um que resolveu. Pra praticar, criei uma tarefa completa no formato Terminal-Bench 2 / Harbor (usado pra medir agentes de código), num domínio que já me é familiar: dados de chuva — transformando um CSV de precipitação diária em um resumo JSON (total de chuva, dias de chuva extrema e o dia mais chuvoso). A tarefa é simples de propósito, porque o foco não é o problema, é a qualidade da avaliação:

✅ Ambiente reproduzível — roda idêntico em qualquer máquina (imagem fixada por digest)
✅ Avaliação honesta — o teste recalcula a resposta certa a partir dos dados, em vez de só checar se um arquivo existe
✅ Consistência ponta a ponta — instrução, configuração, solução e teste apontam pra mesma coisa
✅ Um teste por critério — cada regra da instrução tem exatamente um teste correspondente

A prova de que a tarefa é justa: a solução de referência recebe nota máxima e um "agente vazio" é corretamente reprovado. O que mais me marcou é que engenharia de avaliação de IA mistura rigor de testes, atenção a detalhe e clareza de comunicação — e é uma área que só cresce à medida que agentes de IA entram em produção.

Exemplo completo no GitHub 👇 [LINK DO REPO]

#InteligenciaArtificial #AIEngineering #MachineLearning #LLM #AprendizadoContínuo

---

## 🇬🇧 English

🛠️ I spent some time learning how the quality of AI agents is evaluated — and decided to build an example from scratch to make it stick.

AI models that carry out tasks (the "agents") have to be tested in controlled challenges. But there's a detail few people mention: a badly built test gives a misleading result — it can pass an agent that solved nothing, or fail one that solved it. To practice, I authored a complete task in the Terminal-Bench 2 / Harbor format (used to measure coding agents), in a domain that's already familiar to me: rainfall data — turning a CSV of daily precipitation into a JSON summary (total rainfall, extreme-rain days, and the wettest day). The task is deliberately simple, because the point isn't the problem — it's the quality of the evaluation:

✅ Reproducible environment — runs identically on any machine (base image pinned by digest)
✅ Honest verification — the test recomputes the correct answer from the data, instead of just checking a file exists
✅ End-to-end consistency — instruction, config, solution and test all point to the same thing
✅ One test per criterion — each rule in the instruction maps to exactly one test

The proof that the task is fair: the reference solution scores full marks and a "do-nothing agent" is correctly failed. What struck me most is that AI evaluation engineering blends testing rigor, attention to detail, and clear communication — and it's a field that only grows as AI agents move into production.

Full example on GitHub 👇 [REPO LINK]

#AIEngineering #MachineLearning #LLM #ClimateTech

---

## Dicas
- Troque `[LINK DO REPO]` / `[REPO LINK]` pelo link depois de subir o repo.
- Um screenshot do resultado (reward 1 / reward 0) ou do README aumenta o alcance.
