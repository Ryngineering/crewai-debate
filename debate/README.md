# Debate Crew

Welcome to the Debate Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

**Add your `OPENAI_API_KEY` into the `.env` file.**

---

## Configuration Reference

Quick reference for how each config file and module fits together.

### 1. `src/debate/config/agents.yaml`

Defines **agents**: their identity, behavior, and model. Each agent is a top-level key.

| Key        | Purpose |
|-----------|---------|
| `role`    | Short role label (e.g. "A compelling debater") |
| `goal`    | What the agent should achieve; can use placeholders like `{topic}` |
| `backstory` | Personality and context; same placeholders as `main.py` inputs |
| `model`   | LLM to use (e.g. `openai/gpt-4o-mini`) |

**Placeholders:** Any `{name}` in goal/backstory is filled from the `inputs` dict passed in `main.py` (e.g. `topic`).

**Example structure:**
```yaml
<agent_key>:
  role: >
    Short role description
  goal: >
    Objective, can use {topic} or other input vars.
  backstory: >
    Context and personality. Topic is {topic}.
  model: >
    openai/gpt-4o-mini
```

- Add a new agent by adding a new top-level block and a matching `@agent` method in `crew.py`.

---

### 2. `src/debate/config/tasks.yaml`

Defines **tasks**: what to do, who does it, and where output goes. Each task is a top-level key.

| Key               | Purpose |
|-------------------|---------|
| `description`     | Instructions for the task; can use `{topic}` etc. |
| `expected_output` | What a good result looks like (concise description) |
| `agent`           | Which agent runs this task (must match a key in `agents.yaml`) |
| `output_file`     | Optional; path to write task output (e.g. `output/propose.md`) |

**Execution order:** Determined by the order of `@task` methods in `crew.py` (and `process=Process.sequential`), not by the order in this file.

**Example structure:**
```yaml
<task_key>:
  description: >
    Instructions, can use {topic}.
  expected_output: >
    Brief description of desired output.
  agent: <agent_key>
  output_file: output/<name>.md
```

- Add a new task by adding a block here and a corresponding `@task` method in `crew.py`.

---

### 3. `src/debate/crew.py`

Wires agents and tasks into a **Crew** using the `@CrewBase` pattern.

| Piece | Purpose |
|-------|---------|
| `@CrewBase` class | Loads `agents.yaml` and `tasks.yaml` into `self.agents_config` and `self.tasks_config`. |
| `@agent` methods | Build one `Agent` per agent config; return `Agent(config=self.agents_config['<key>'], verbose=True, ...)`. |
| `@task` methods | Build one `Task` per task config; return `Task(config=self.tasks_config['<key>'], output_file=...)`. Override `output_file` here if you don’t want the YAML value. |
| `@crew` method | Build the `Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, ...)`. |

**Flow:**
1. YAML defines content (role, goal, tasks, etc.).
2. `crew.py` maps each YAML entry to an `Agent` or `Task` and optionally overrides options (e.g. `output_file`).
3. `main.py` calls `Debate().crew().kickoff(inputs=...)` and passes `inputs` for placeholders.

**Useful options:**
- `process=Process.sequential` — tasks run in the order they appear in `self.tasks`.
- `process=Process.hierarchical` — manager assigns tasks (see crewAI docs).
- Add tools to an agent: pass `tools=[...]` in the `Agent(...)` call.

---

### 4. `src/debate/main.py`

Entrypoint for running, training, and testing the crew. The **inputs** dict is what fills placeholders in `agents.yaml` and `tasks.yaml` (e.g. `{topic}`).

| Function | Purpose |
|----------|---------|
| `run()` | Default: `kickoff(inputs={'topic': '...'})`. Use for normal runs. |
| `train(n_iterations, filename, inputs)` | Train the crew; iterations and filename from `sys.argv[1]`, `sys.argv[2]`. |
| `replay(task_id)` | Replay from a given task; `task_id` from `sys.argv[1]`. |
| `test(n_iterations, eval_llm, inputs)` | Test run; iterations and eval model from `sys.argv[1]`, `sys.argv[2]`. |
| `run_with_trigger()` | Run with JSON payload in `sys.argv[1]`; payload merged into `inputs`. |

**To change the debate topic:** Edit the `inputs` dict in `run()` (and in `train()`/`test()` if you use them), e.g. `'topic': 'Your debate topic here'`.

---

## Running the Project

From the project root:

```bash
crewai run
```

This builds the Debate crew from `agents.yaml` and `tasks.yaml`, runs the tasks in sequence, and writes outputs (e.g. `output/propose.md`, `output/oppose.md`, `output/decide.md`, or `report.md` depending on overrides in `crew.py`).

---

## Understanding Your Crew

The debate crew has:

- **Agents:** `debater` (argues for/against) and `judge` (picks a winner from the arguments).
- **Tasks:** `propose` (for), `oppose` (against), `decide` (judge chooses winner). They run in that order with `Process.sequential`.

All of this is driven by `agents.yaml`, `tasks.yaml`, `crew.py`, and the `inputs` in `main.py` as described above.

---

## Support

For support, questions, or feedback regarding the Debate Crew or crewAI:

- [Documentation](https://docs.crewai.com)
- [GitHub](https://github.com/joaomdmoura/crewai)
- [Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with docs](https://chatg.pt/DWjSBZn)
