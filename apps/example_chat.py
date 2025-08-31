"""
Example Streamlit Chat App with Claude Code Agent

A simple chat interface demonstrating the use of headless Claude Code SDK.
"""

import asyncio
from pathlib import Path

import streamlit as st
from agent import AgentConfig, AuthManager, AuthMethod, ClaudeAgent, SessionManager, SubAgentManager, ToolManager
from agent.client import OutputFormat, PermissionMode
from agent.tools import Tool


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()

    if "tool_manager" not in st.session_state:
        st.session_state.tool_manager = ToolManager()

    if "subagent_manager" not in st.session_state:
        st.session_state.subagent_manager = SubAgentManager()

    if "auth_manager" not in st.session_state:
        st.session_state.auth_manager = AuthManager()

    if "current_session" not in st.session_state:
        st.session_state.current_session = None

    if "agent_config" not in st.session_state:
        st.session_state.agent_config = AgentConfig(
            output_format=OutputFormat.TEXT, permission_mode=PermissionMode.DEFAULT, working_directory=Path.cwd()
        )


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.header("Configuration")

        # Authentication Status
        st.subheader("Authentication Status")
        auth_status = st.session_state.auth_manager.detect_auth_method()

        # Display auth method with color-coded status
        if auth_status.is_authenticated:
            st.success(f"✅ {auth_status.details.get('method', 'Unknown')}")
        else:
            st.error("❌ Not Authenticated")

        # Display auth details
        with st.expander("Authentication Details", expanded=not auth_status.is_authenticated):
            if auth_status.method == AuthMethod.AMAZON_BEDROCK:
                st.write("**Method:** Amazon Bedrock")
                st.write(f"**Region:** {auth_status.details.get('aws_region', 'Not set')}")
                st.write(f"**Credential Source:** {auth_status.details.get('credential_source', 'Unknown')}")
                st.write(f"**Primary Model:** {auth_status.details.get('primary_model', 'Default')[:50]}...")
            elif auth_status.method == AuthMethod.ANTHROPIC_API:
                st.write("**Method:** Anthropic API")
                st.write(f"**API Key:** {auth_status.details.get('api_key', 'Not set')}")
                st.write(f"**API Base:** {auth_status.details.get('api_base', 'Default')}")
            elif auth_status.method == AuthMethod.CLAUDE_ACCOUNT:
                st.write("**Method:** Claude Account")
                st.write(f"**Subscription:** {auth_status.details.get('subscription', 'Unknown')}")
                if "login_method" in auth_status.details:
                    st.write(f"**Login Method:** {auth_status.details['login_method']}")
                if "account_type" in auth_status.details:
                    st.write(f"**Account Type:** {auth_status.details['account_type']}")
                if "current_model" in auth_status.details:
                    st.write(f"**Model:** {auth_status.details['current_model']}")
                if auth_status.details.get("status_command_working"):
                    st.write("**Status:** /status command working ✅")
                if "doctor_output" in auth_status.details:
                    st.write(f"**Doctor Info:** {auth_status.details['doctor_output'][:100]}...")
            else:
                st.write("**Method:** None configured")

            if auth_status.error:
                st.error(auth_status.error)

            # Show configuration instructions if not authenticated
            if not auth_status.is_authenticated:
                st.write("**Configuration Instructions:**")
                instructions = st.session_state.auth_manager.get_configuration_instructions(auth_status.method)
                st.code(instructions, language="markdown")

        # Refresh button
        if st.button("🔄 Refresh Auth Status"):
            st.session_state.auth_manager.refresh_status()
            st.rerun()

        st.divider()

        # Tool Profile Selection
        st.subheader("Tool Profile")
        profiles = st.session_state.tool_manager.list_profiles()
        selected_profile = st.selectbox("Select tool profile", options=profiles, index=profiles.index("full_access"))

        if st.button("Apply Profile"):
            st.session_state.tool_manager.apply_profile(selected_profile)
            st.success(f"Applied {selected_profile} profile")

        # Display current profile info
        profile_info = st.session_state.tool_manager.get_profile_info(selected_profile)
        if profile_info:
            st.info(profile_info["description"])

        # Session Management
        st.subheader("Session Management")

        if st.button("New Session"):
            session = st.session_state.session_manager.create_session()
            st.session_state.current_session = session
            st.session_state.messages = []
            st.success("Created new session")

        # List existing sessions
        sessions = st.session_state.session_manager.list_sessions()
        if sessions:
            st.write("Recent Sessions:")
            for session in sessions[:5]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"{session['title'][:30]}...")
                with col2:
                    if st.button("Load", key=f"load_{session['id']}"):
                        loaded_session = st.session_state.session_manager.load_session(session["id"])
                        st.session_state.current_session = loaded_session
                        # Restore conversation history
                        st.session_state.messages = [
                            {"role": turn.role, "content": turn.content} for turn in loaded_session.turns
                        ]
                        st.rerun()

        # Agent Configuration
        st.subheader("Agent Settings")

        permission_mode = st.selectbox(
            "Permission Mode", options=[mode.value for mode in PermissionMode], index=2  # Default to DEFAULT
        )
        st.session_state.agent_config.permission_mode = PermissionMode(permission_mode)

        output_format = st.selectbox(
            "Output Format", options=[fmt.value for fmt in OutputFormat], index=0  # Default to TEXT
        )
        st.session_state.agent_config.output_format = OutputFormat(output_format)

        # System Prompt
        system_prompt = st.text_area(
            "System Prompt (optional)", value=st.session_state.agent_config.system_prompt or "", height=100
        )
        if system_prompt:
            st.session_state.agent_config.system_prompt = system_prompt

        # Subagents
        st.subheader("Available Subagents")
        agents_list = st.session_state.subagent_manager.list_agents()

        for category, agents in agents_list.items():
            if agents:
                st.write(f"**{category.title()}:**")
                for agent_name in agents:
                    agent = st.session_state.subagent_manager.get_agent(agent_name)
                    if agent:
                        with st.expander(agent_name):
                            st.write(agent.description)
                            if agent.proactive:
                                st.info("Proactive agent")


def render_chat():
    """Render the main chat interface."""
    st.title("Claude Code Agent Chat")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask Claude Code..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Save to session
        if st.session_state.current_session:
            st.session_state.session_manager.add_turn("user", prompt)

        # Get Claude response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Configure agent with current settings
            st.session_state.agent_config.allowed_tools = [
                Tool[tool] for tool in st.session_state.tool_manager.allowed_tools
            ]
            st.session_state.agent_config.disallowed_tools = [
                Tool[tool] for tool in st.session_state.tool_manager.disallowed_tools
            ]

            agent = ClaudeAgent(st.session_state.agent_config, auth_manager=st.session_state.auth_manager)

            # Execute query asynchronously
            try:
                # Get resume ID from current session
                resume_id = None
                if st.session_state.current_session:
                    resume_id = st.session_state.current_session.conversation_id

                # Run async query
                async def run_query():
                    response_parts = []
                    async for chunk in agent.query(prompt, resume_id):
                        response_parts.append(chunk)
                    return "".join(response_parts)

                # Execute in event loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                full_response = loop.run_until_complete(run_query())
                loop.close()

                # Update conversation ID
                if agent.conversation_id and st.session_state.current_session:
                    st.session_state.session_manager.update_conversation_id(agent.conversation_id)

                message_placeholder.markdown(full_response)

            except Exception as e:
                message_placeholder.error(f"Error: {str(e)}")
                full_response = f"Error: {str(e)}"

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save to session
        if st.session_state.current_session:
            st.session_state.session_manager.add_turn("assistant", full_response)


def main():
    """Main application entry point."""
    st.set_page_config(page_title="Claude Code Agent Chat", page_icon="🤖", layout="wide")

    initialize_session_state()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
