# Analyzuj repozitář kurzu

Tento příkaz projde lokální repo kurzu a pro vybranou lekci vytvoří souhrnný popis, který pak používají ostatní příkazy.

## Použití
`/analyzuj-repo $ARGUMENTS`

kde `$ARGUMENTS` je:
- `<cesta> <číslo-lekce>` — zpracuje jen jednu lekci, např. `/home/michal/projects/Vibe-Coding-1 4`
- `<cesta>` — zpracuje všechny lekce (paralelně přes subagenty)

## Detekce složek lekce

Názvy složek v repo nejsou fixní — mohou mít libovolnou formu (`1_LLM/`, `1-llm-intro/`, `01_basics/` apod.).

**Před každým zpracováním** spusť:
```bash
ls <REPO_PATH>/
```
a z výstupu identifikuj složky začínající číslicí. Číslo na začátku = číslo lekce. Ignoruj složky bez číselného prefixu (např. `scripts/`, `.git/`).

Orientační témata podle čísla lekce (názvy složek se mohou lišit):

| Číslo | Téma |
|-------|------|
| 1 | Základy LLM — API volání |
| 2 | Codex — tools, MCP, skills, hooks |
| 3 | Codex SDK (TypeScript) |
| 4 | Claude Code — tools, MCP, skills, hooks |
| 5 | Claude Agent SDK (Python + TypeScript) |
| 6 | Ostatní agenti (Copilot, Gemini CLI, Cursor) |
| 7 | Office suite — grafy, obrázky, videa, dokumenty |
| 8 | Praktické kódování — spec-kit, Ralph Wiggum |

## Postup — jedna lekce

Pokud je zadáno číslo lekce, zpracuj ji přímo (bez subagenta):

1. Spusť `ls <REPO_PATH>/` a najdi složku s odpovídajícím číselným prefixem
2. Přečti strom složek do hloubky 3 od složky lekce
3. Pro každý adresář přečti: `README.md`, `main.py`, `AGENTS.md`, `SKILL.md` vždy; ostatní `.ts`/`.py` jen pokud jsou hlavní soubory projektu; z `package.json` jen `name`, `description`, `scripts`
4. `SKILL.md` hledej rekurzivně do libovolné hloubky
5. Přeskoč: `node_modules/`, `.venv/`, `__pycache__/`, `.git/`, `dist/`, `build/`, `*.lock`
6. Zapiš výsledek do `repo-summary/lekce-XX-repo.md`

## Postup — všechny lekce (subagenti)

Pokud číslo lekce **není** zadáno, spusť pro každou lekci samostatný subagent paralelně.

Nejdříve spusť `ls <REPO_PATH>/` a identifikuj všechny složky s číselným prefixem. Pro každou nalezenou složku spusť tento bash příkaz (všechny paralelně jako samostatné Bash tool cally):

```bash
claude --print --allowedTools "Read,Bash" \
  "Analyze the repository folder at <REPO_PATH>/<FOLDER> for lesson <N>.

Read the folder tree to depth 3. For each directory read: README.md, main.py, AGENTS.md, SKILL.md always; other .ts/.py only if they are the main project files; from package.json only name/description/scripts fields. Search for SKILL.md recursively at any depth. Skip: node_modules/, .venv/, __pycache__/, .git/, dist/, build/, *.lock files.

Special rules:
- Lessons 3 and 5 (SDK): process both python/ and typescript/ subfolders
- Lesson 8 (8_Practical_Code): monorepo — describe top-level structure, do not read all TS files deeply

Return ONLY the content of the repo-summary file in this exact format (nothing else):

# Lekce <N> — Repo summary: <FOLDER>

## Přehled
What this part of the repository contains and demonstrates.

## Struktura složky
Overview of subfolders and their purpose.

## Klíčové soubory
- \`path/file.py\` — what it demonstrates, main concept

## Koncepty demonstrované v kódu
- list of concepts shown (structured output, MCP, subagents...)

## Poznámky
Anything interesting worth noting (unusual approaches, differences from other lessons...)"
```

Po dokončení všech subagentů:
- Zapiš výstup každého subagenta do `repo-summary/lekce-XX-repo.md`
- Subagenti vrátí pouze obsah souboru — žádné jiné výstupy neočekávej

## Formát repo-summary souboru

```
# Lekce XX — Repo summary: [název složky]

## Přehled
Co tato část repozitáře obsahuje a demonstruje.

## Struktura složky
Přehled podsložek a k čemu slouží.

## Klíčové soubory
- `cesta/soubor.py` — co demonstruje, jaký je hlavní koncept
- `cesta/soubor.ts` — ...

## Koncepty demonstrované v kódu
- seznam toho co kód ukazuje (structured output, MCP, subagents...)

## Poznámky
Cokoli zajímavého co stojí za zmínku (neobvyklé přístupy, rozdíly oproti jiným lekcím...)
```

## Na konci vypiš
- Seznam vytvořených repo-summary souborů
- Zda byly použity subagenti (ano při zpracování všech lekcí)
- Případné složky které nebyly jasné nebo neměly README
