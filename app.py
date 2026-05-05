import streamlit as st
from agent import run_travel_agent_with_steps, critic_agent

st.title("Agentic Travel Planner (MCP)")

query = st.text_input("Describe your trip")
budget_limit = st.number_input(
    "💰 Budget maximum (USD)",
    min_value=0,
    max_value=10000,
    value=500,
    step=50
)

if st.button("Plan My Trip"):
    if query:
        with st.spinner("L'agent planifie votre voyage..."):
            final_output, steps = run_travel_agent_with_steps(query)

        # Affichage des outils
        st.subheader("🔧 Outils utilisés par l'agent")
        for i, step in enumerate(steps):
            with st.expander(f"Étape {i+1} — {step['tool']}"):
                st.write("**Arguments :**", step['args'])
                st.write("**Résultat :**", step['result'])

        # Exercice 3 : vérification du budget
        import re
        amounts = re.findall(r'\$(\d+(?:\.\d+)?)', final_output)
        estimated = max([float(a) for a in amounts]) if amounts else 0

        if estimated > budget_limit and budget_limit > 0:
            st.warning(f"⚠️ Budget estimé (${estimated}) dépasse votre limite (${budget_limit}). Re-planification...")
            new_query = f"{query}. IMPORTANT: the total budget must not exceed ${budget_limit} USD. Suggest cheaper alternatives."
            with st.spinner("Re-planification en cours..."):
                final_output, steps = run_travel_agent_with_steps(new_query)
            st.success("✅ Plan re-planifié dans le budget !")

            st.subheader("🔧 Outils utilisés (re-planification)")
            for i, step in enumerate(steps):
                with st.expander(f"Étape {i+1} — {step['tool']}"):
                    st.write("**Arguments :**", step['args'])
                    st.write("**Résultat :**", step['result'])

        # Plan final
        st.subheader("📋 Travel Plan")
        st.write(final_output)

        # Exercice 2 : agent critique
        st.subheader("🧐 Évaluation par l'agent critique")
        with st.spinner("L'agent critique analyse le plan..."):
            critique = critic_agent(final_output)
        st.info(critique)

    else:
        st.warning("Entre une description de voyage d'abord !")