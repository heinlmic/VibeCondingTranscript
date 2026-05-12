# Analyzuj repozitář kurzu

Tento příkaz projde lokální repo kurzu a pro vybranou lekci vytvoří souhrnný popis, který pak používají ostatní příkazy.

## Použití
`/analyzuj-repo $ARGUMENTS`

kde `$ARGUMENTS` je:
- `<cesta> <číslo-lekce>` — zpracuje jen jednu lekci, např. `/home/michal/projects/Vibe-Coding-1 4`
- `<cesta>` — zpracuje všechny lekce

## Mapování číslo lekce → složka v repo

| Číslo | Složka | Téma |
|-------|--------|------|
| 1 | `1_LLM/` | Základy LLM — API volání |
| 2 | `2_Codex/` | Codex — tools, MCP, skills, hooks |
| 3 | `3_Codex_SDK/typescript/` | Codex SDK (TypeScript) |
| 4 | `4_Claude_Code/` | Claude Code — tools, MCP, skills, hooks |
| 5 | `5_Claude_Agent_SDK/` | Claude Agent SDK (Python + TypeScript) |
| 6 | `6_Others/` | Ostatní agenti (Copilot, Gemini CLI, Cursor) |
| 7 | `7_Practical_Office_suite/` | Office suite — grafy, obrázky, videa, dokumenty |
| 8 | `8_Practical_Code/` | Praktické kódování — spec-kit, Ralph Wiggum |

## Postup

1. Zkontroluj argumenty:
   - Pokud je zadáno číslo lekce, zpracuj jen odpovídající složku z tabulky výše
   - Pokud číslo není zadáno, zpracuj všechny složky ze tabulky

2. Pro každou zpracovávanou složku lekce:
   a. Přečti strom složek **do hloubky 3 úrovní** od složky lekce (ne od kořene repo)
   b. Pro každý nalezený adresář (úrovně 1–3) přečti tyto soubory pokud existují:
      - `README.md` — vždy čti
      - `main.py` — vždy čti
      - `AGENTS.md`, `SKILL.md` — vždy čti
      - `*.ts`, `*.py` (ostatní) — čti jen pokud jsou to hlavní soubory projektu (ne utility v hlubokých podsložkách)
      - `package.json` — přečti jen pole `name`, `description`, `scripts` (ne `dependencies`)
   c. SKILL.md hledej **rekurzivně** do libovolné hloubky — mohou být zanořeny 10+ úrovní hluboko v plugin složkách

3. Přeskoč tyto složky a soubory **zcela**:
   - Složky: `node_modules/`, `.venv/`, `__pycache__/`, `.git/`, `dist/`, `build/`
   - Soubory: `uv.lock`, `package-lock.json`, `tsconfig.json`, `*.lock`, `.gitignore`, `*.env`
   - Pro `pyproject.toml` a `uv.lock`: jen zaznamenej že projekt používá uv/pip (nečti obsah)

4. Speciální chování pro konkrétní lekce:
   - **Lekce 3 a 5** (`*_SDK`): mají podsložky `python/` a `typescript/` — procházej obě
   - **Lekce 8** (`8_Practical_Code`): monorepo struktura (`apps/`, `packages/`) — uveď strukturu a top-level README, nečti všechny TS soubory do hloubky

5. Pro každou zpracovávanou lekci vytvoř `repo-summary/lekce-XX-repo.md`

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
- Případné složky které nebyly jasné nebo neměly README
