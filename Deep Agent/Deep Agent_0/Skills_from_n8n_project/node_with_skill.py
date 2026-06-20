"""
Branchement d'un Skill (SKILL.md) dans un nœud LangGraph
==========================================================

Idée : le nœud LangGraph ne contient plus le prompt en dur. Il invoque
le Claude Agent SDK (`query()`), qui lui-même découvre et charge le
skill `documentation-algo` depuis le filesystem, et choisit la bonne
référence (sql-analysis-rules.md / business-vocabulary.md / ...)
selon l'étape demandée dans le prompt utilisateur.

Le accept/deny, lui, reste entièrement dans LangGraph (interrupt() +
Command(goto=...)) -- voir n8n_equivalent_langgraph.py. Le skill ne sait
même pas qu'une boucle de validation existe autour de lui.

Pré-requis :
    npm install -g @anthropic-ai/claude-code   # le SDK l'utilise en sous-main
    pip install claude-agent-sdk
"""

import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import AssistantMessage, TextBlock


async def run_skill_agent(prompt: str, project_dir: str) -> str:
    """
    Lance un agent Claude équipé du skill 'documentation-algo' trouvé
    dans <project_dir>/skills/, et retourne sa réponse texte complète.
    """
    options = ClaudeAgentOptions(
        # "project" indique au SDK de scanner project_dir/.claude/skills
        # ou project_dir/skills selon la convention -> ici on utilise
        # directement cwd pointé sur le dossier contenant skills/.
        setting_sources=["user", "project"],
        cwd=project_dir,
        # "Skill" DOIT être dans allowed_tools, sinon le skill est invisible
        # pour l'agent même s'il est présent sur le disque.
        allowed_tools=["Skill", "Read"],
        permission_mode="acceptEdits",
        system_prompt={"type": "preset", "preset": "claude_code"},
        model="claude-sonnet-4-6",
    )

    result_text = ""
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    result_text += block.text
    return result_text


# ---------------------------------------------------------------------------
# Nœud LangGraph -- remplace l'ancien sql_agent_node() qui avait le prompt
# en dur. La logique d'orchestration (state, interrupt, edges) ne change
# pas d'un caractère : seul le CONTENU du nœud change.
# ---------------------------------------------------------------------------

PROJECT_DIR = "/home/claude/deepagents_demo"  # contient ./skills/documentation-algo


def sql_agent_node_with_skill(state: dict) -> dict:
    """
    Équivalent du node n8n 'Agent SQL', mais le prompt système n'est plus
    en dur dans le code Python : il vient du SKILL.md découvert par le
    Claude Agent SDK au moment de l'appel.
    """
    comment_block = (
        f"\nL'utilisateur a un commentaire : {state['user_comment']}"
        if state.get("user_comment")
        else ""
    )

    # On ne décrit PAS les règles SQL ici -- on demande juste l'étape.
    # C'est le skill qui sait quel fichier de référence charger pour
    # "analyse technique du SQL".
    prompt = (
        f"Effectue l'analyse technique (étape 1 : analyse syntaxique SQL) "
        f"du script suivant :\n\n{state['sql_text']}{comment_block}"
    )

    technical_doc = asyncio.run(run_skill_agent(prompt, PROJECT_DIR))
    return {"technical_doc": technical_doc, "user_comment": None}


if __name__ == "__main__":
    # Test isolé du nœud, hors graphe complet.
    fake_state = {
        "sql_text": "SELECT * INTO #tmp FROM FtDelivery WHERE ValidityFlag = 1",
        "user_comment": None,
    }
    output = sql_agent_node_with_skill(fake_state)
    print(output["technical_doc"])
