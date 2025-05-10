
import streamlit as st
import json
import pandas as pd
import os
import random
import datetime
import shutil

# Constants
DATA_FILE = "agent_metadata_summary.json"
STATE_FILE = "agent_mutation_state.json"
SECRETS_FILE = "170_custom_chat_gpt_secrets.txt"
METHODS_FILE = "200_intelligent_methods.txt"
CONDITIONS_FILE = "generated_500_condition_statements.json"
LOG_FILE = "mutation_log.json"

# Backup on launch
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
if os.path.exists(STATE_FILE):
    shutil.copyfile(STATE_FILE, f"agent_mutation_state_backup_{timestamp}.json")

# Load metadata
with open(DATA_FILE, "r") as f:
    metadata = json.load(f)

# Load or initialize mutation state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        agent_state = json.load(f)
else:
    agent_state = {agent["id"]: agent for agent in metadata}
    with open(STATE_FILE, "w") as f:
        json.dump(agent_state, f, indent=2)

# Load log file or create new
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        mutation_log = json.load(f)
else:
    mutation_log = []

# Load resources
def load_lines(file_path, limit=None):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines[:limit] if limit else lines

gpt_secrets = load_lines(SECRETS_FILE)
intelligent_methods = load_lines(METHODS_FILE)
condition_statements = load_lines(CONDITIONS_FILE, 100)

# Streamlit Layout
st.set_page_config(page_title="🧠 TeleSkill Ultra+ Logger", layout="wide")
st.title("🧠 TeleSkill Ultra Dashboard · Logging & Resilience")

df = pd.DataFrame(agent_state.values())

st.sidebar.header("🔎 Filters")
domains = df["domain"].dropna().unique()
personalities = df["personality"].dropna().unique()

selected_domains = st.sidebar.multiselect("Domain", domains, default=list(domains))
selected_personalities = st.sidebar.multiselect("Personality", personalities, default=list(personalities))

filtered_df = df[df["domain"].isin(selected_domains) & df["personality"].isin(selected_personalities)]
st.write(f"Showing {len(filtered_df)} agents")
st.dataframe(filtered_df)

agent_ids = filtered_df["id"].tolist()
selected_agent_id = st.selectbox("Choose Agent", agent_ids)

def log_action(agent_id, action_type, description):
    entry = {
        "agent_id": agent_id,
        "action": action_type,
        "description": description,
        "timestamp": datetime.datetime.now().isoformat()
    }
    mutation_log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(mutation_log, f, indent=2)

if selected_agent_id:
    agent = agent_state[selected_agent_id]
    st.subheader(f"🧬 Agent: {selected_agent_id}")
    st.json(agent)

    st.markdown("### ⚙️ Mutation Controls")

    if st.button("🔁 Shift Personality"):
        old = agent["personality"]
        agent["personality"] = "adaptive-strategic"
        st.success(f"{old} → {agent['personality']}")
        log_action(selected_agent_id, "personality_shift", f"{old} → {agent['personality']}")

    if st.button("🎯 Add RL Hook"):
        agent["intent"] += "_rlhook"
        st.info(f"Intent updated: {agent['intent']}")
        log_action(selected_agent_id, "intent_reinforce", agent["intent"])

    if st.button("🧱 Optimize Domain"):
        agent["domain"] += " [Optimized]"
        st.success(f"Domain now: {agent['domain']}")
        log_action(selected_agent_id, "domain_tagged", agent["domain"])

    if st.button("🧠 Inject Super Logic + Secrets"):
        agent["intelligent_method"] = random.choice(intelligent_methods)
        agent["ultra_secrets"] = gpt_secrets
        agent["condition_statements"] = random.sample(condition_statements, 3)
        st.success("Logic, conditions, and secrets injected.")
        log_action(selected_agent_id, "logic_injection", "3 conditions, secrets, intelligent method")

    with open(STATE_FILE, "w") as f:
        json.dump(agent_state, f, indent=2)

st.markdown("---")
st.caption("Quantum GPT Stack · Mutation Logger Enabled")
