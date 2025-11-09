import pandas as pd
import streamlit as st

from src.application.query_manager import QueryManager


class Index:

    def __init__(self, query_manager: QueryManager):
        self.query_manager = query_manager

    def render(self):

        st.set_page_config(
            page_title="LLM Único vs Multiagentes - Estudo Comparativo",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.markdown(
            """
            <style>
                :root {
                    --llm-color: #3B82F6;
                    --multiagent-color: #10B981;
                    --accent-color: #8B5CF6;
                    --text-color: #F3F4F6;
                    --dark-bg: #000000;
                    --card-bg: rgba(30, 41, 59, 0.8);
                    --card-hover: rgba(30, 41, 59, 1);
                    --border-radius: 12px;
                }

                .stApp {
                    background: var(--dark-bg);
                    color: var(--text-color);
                }

                .header-section {
                    text-align: center;
                    padding: 2rem 0;
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
                    border-radius: var(--border-radius);
                    margin-bottom: 2rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }

                .header-title {
                    font-size: 2.5rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, var(--llm-color), var(--multiagent-color));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 0.5rem;
                }

                .header-subtitle {
                    color: #94A3B8;
                    font-size: 1.1rem;
                    margin-bottom: 1rem;
                }

                .comparison-badge {
                    display: inline-block;
                    padding: 0.5rem 1rem;
                    background: rgba(139, 92, 246, 0.2);
                    border: 1px solid var(--accent-color);
                    border-radius: 20px;
                    font-size: 0.9rem;
                    color: var(--accent-color);
                }

                .approach-card {
                    background: var(--card-bg);
                    border-radius: var(--border-radius);
                    padding: 1.5rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    transition: all 0.3s ease;
                    height: 100%;
                    margin-bottom: 1rem;
                }

                .approach-card:hover {
                    transform: translateY(-5px);
                    border-color: rgba(255, 255, 255, 0.2);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                }

                .llm-card {
                    border-top: 4px solid var(--llm-color);
                }

                .multiagent-card {
                    border-top: 4px solid var(--multiagent-color);
                }

                .approach-icon {
                    font-size: 2rem;
                    margin-bottom: 1rem;
                }

                .approach-title {
                    font-size: 1.3rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    color: var(--text-color);
                }

                .approach-description {
                    color: #94A3B8;
                    font-size: 0.9rem;
                    line-height: 1.5;
                    margin-bottom: 1.5rem;
                }

                .stTextArea textarea {
                    min-height: 200px !important;
                    border-radius: 8px !important;
                    border: 1px solid #374151 !important;
                    background-color: #1E293B !important;
                    color: var(--text-color) !important;
                    font-family: 'Courier New', monospace !important;
                }

                .stButton button {
                    width: 100%;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    border: none;
                }

                .llm-button {
                    background: linear-gradient(135deg, var(--llm-color), #2563EB) !important;
                    color: white !important;
                }

                .multiagent-button {
                    background: linear-gradient(135deg, var(--multiagent-color), #059669) !important;
                    color: white !important;
                }

                .stButton button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                }

                .result-section {
                    background: rgba(30, 41, 59, 0.6);
                    border-radius: var(--border-radius);
                    padding: 1.5rem;
                    margin-top: 1rem;
                    border-left: 4px solid var(--accent-color);
                }

                .metric-badge {
                    display: inline-flex;
                    align-items: center;
                    padding: 0.4rem 0.8rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 20px;
                    font-size: 0.8rem;
                    margin-right: 0.5rem;
                    margin-bottom: 0.5rem;
                }

                .footer {
                    text-align: center;
                    padding: 2rem 0;
                    color: #64748B;
                    font-size: 0.9rem;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    margin-top: 3rem;
                }

                .comparison-stats-3 {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 1.5rem;
                    margin: 2rem 0;
                }

                .stat-card-3 {
                    background: rgba(30, 41, 59, 0.9);
                    padding: 1.5rem;
                    border-radius: var(--border-radius);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    transition: all 0.3s ease;
                    height: 55vh;
                    margin-bottom: 1rem;
                }

                .stat-card-3:hover {
                    transform: translateY(-5px);
                    border-color: rgba(255, 255, 255, 0.3);
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                }

                .metric-icon-3 {
                    font-size: 2.8rem;
                    margin-bottom: 1rem;
                    text-align: center;
                }

                .stat-value-3 {
                    font-size: 1.8rem;
                    font-weight: 700;
                    text-align: center;
                    margin-bottom: 0.5rem;
                }

                .stat-label-3 {
                    font-size: 1.1rem;
                    font-weight: 600;
                    text-align: center;
                    margin-bottom: 1rem;
                    color: var(--text-color);
                }

                .stat-description-3 {
                    font-size: 0.85rem;
                    color: #94A3B8;
                    line-height: 1.5;
                    text-align: left;
                }

                .coverage-card {
                    border-top: 4px solid #10B981;
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(30, 41, 59, 0.9));
                }

                .time-card {
                    border-top: 4px solid #3B82F6;
                    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(30, 41, 59, 0.9));
                }

                .mutation-card {
                    border-top: 4px solid #8B5CF6;
                    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(30, 41, 59, 0.9));
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # Header Section
        st.markdown(
            """
            <div class="header-section">
                <div class="header-title">LLM Único vs Sistemas Multiagentes</div>
                <div class="header-subtitle">Estudo Comparativo em Geração de Testes Unitários e Qualidade de Software</div>
                <div class="comparison-badge">Análise de Métricas Técnicas Especializadas</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Cards das 3 métricas principais em colunas
        st.markdown("### 📈 Métricas Principais do Estudo")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                <div class="stat-card-3 coverage-card">
                    <div class="metric-icon-3">📊</div>
                    <div class="stat-value-3">Code Coverage</div>
                    <div class="stat-label-3">Cobertura de Código</div>
                    <div class="stat-description-3">
                        <strong>Objetivo:</strong> Medir a porcentagem do código-fonte que é executada pelos testes unitários gerados.
                        <br><br>
                        <strong>Métricas específicas:</strong>
                        <br>• <strong>Linhas</strong>: % de linhas de código executadas
                        <br>• <strong>Branch</strong>: Cobertura de ramificações condicionais
                        <br>• <strong>Funções</strong>: Métodos e funções testadas
                        <br><br>
                        <strong>Importância:</strong> Garante que o código crítico está sendo adequadamente testado.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <div class="stat-card-3 time-card">
                    <div class="metric-icon-3">⏱️</div>
                    <div class="stat-value-3">Tempo de Execução</div>
                    <div class="stat-label-3">Performance</div>
                    <div class="stat-description-3">
                        <strong>Objetivo:</strong> Comparar a eficiência computacional das duas abordagens.
                        <br><br>
                        <strong>Aspectos avaliados:</strong>
                        <br>• <strong>Geração</strong>: Tempo para criar os testes
                        <br>• <strong>Execução</strong>: Tempo da suíte de testes
                        <br>• <strong>Recursos</strong>: Utilização de CPU/GPU
                        <br><br>
                        <strong>Relevância:</strong> Impacto na produtividade e escalabilidade.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
                <div class="stat-card-3 mutation-card">
                    <div class="metric-icon-3">🧬</div>
                    <div class="stat-value-3">Teste de Mutação</div>
                    <div class="stat-label-3">Efetividade</div>
                    <div class="stat-description-3">
                        <strong>Objetivo:</strong> Avaliar a qualidade dos testes através de mutações no código.
                        <br><br>
                        <strong>Processo:</strong>
                        <br>• <strong>Mutantes</strong>: Bugs artificiais inseridos
                        <br>• <strong>Detecção</strong>: Capacidade de identificar erros
                        <br>• <strong>Score</strong>: % de mutantes detectados
                        <br><br>
                        <strong>Valor:</strong> Indicador direto da robustez dos testes.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Resto do código permanece igual...
        # Main Comparison Interface
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                """
                <div class="approach-card llm-card">
                    <div class="approach-icon">🧠</div>
                    <div class="approach-title">LLM Único com Engenharia de Prompt</div>
                    <div class="approach-description">
                        Abordagem tradicional utilizando um único modelo de linguagem com prompts
                        estruturados para geração de testes unitários. Ideal para cenários simples
                        e diretos com requisitos bem definidos.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            query_llm = st.text_area(
                "Código para Análise - LLM Único",
                placeholder="""// Cole seu código aqui para geração de testes unitários
    Exemplo:
    def calcular_media(numeros):
        if not numeros:
            return 0
        return sum(numeros) / len(numeros)""",
                height=200,
                key="llm_input",
            )

            if st.button(
                "🚀 Gerar Testes com LLM Único",
                key="llm_button",
                use_container_width=True,
            ):
                if not query_llm:
                    st.warning("Por favor, insira o código para análise.")
                else:
                    with st.spinner(
                        "🔍 Analisando código e gerando testes unitários..."
                    ):
                        try:
                            result = self.query_manager.unique_llm_response(query_llm)
                            code_response = (
                                result.code or "Não foi possível gerar código."
                            )

                            st.markdown("### 📊 Resultado - LLM Único")

                            with st.expander("Code - LLM Único", expanded=True):
                                if isinstance(code_response, str):
                                    st.code(code_response, language="python")

                            st.download_button(
                                label="📥 Baixar Testes Gerados",
                                data=(
                                    code_response
                                    if isinstance(code_response, str)
                                    else str(code_response)
                                ),
                                file_name="testes_llm_unico.py",
                                mime="text/x-python",
                            )

                        except Exception as e:
                            st.error(f"❌ Erro na geração de testes: {str(e)}")

        with col2:
            st.markdown(
                """
                <div class="approach-card multiagent-card">
                    <div class="approach-icon">🤖</div>
                    <div class="approach-title">Sistema Multiagente Especializado</div>
                    <div class="approach-description">
                        Arquitetura distribuída com múltiplos agentes especializados trabalhando
                        em conjunto para análise de código, planejamento de testes e implementação.
                        Superior em cenários complexos e projetos de grande escala.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            query_multiagent = st.text_area(
                "Código para Análise - Multiagente",
                placeholder="""// Cole seu código aqui para análise multiagente
    Exemplo:
    class GerenciadorUsuarios:
        def __init__(self):
            self.usuarios = []

        def adicionar_usuario(self, usuario):
            # Lógica complexa de validação
            self.usuarios.append(usuario)""",
                height=200,
                key="multiagent_input",
            )

            if st.button(
                "🚀 Gerar Testes com Multiagentes",
                key="multiagent_button",
                use_container_width=True,
            ):
                if not query_multiagent:
                    st.warning("Por favor, insira o código para análise.")
                else:
                    with st.spinner(
                        "🤖 Coordenando agentes especializados para análise..."
                    ):
                        try:
                            result = self.query_manager.multi_agent_response(
                                query_multiagent
                            )
                            code_response = result.code or result.error

                            st.markdown("### 📊 Resultado - Sistema Multiagente")

                            with st.expander("Test Code - Multiagente", expanded=True):
                                if isinstance(code_response, str):
                                    st.code(code_response, language="python")

                            if result.state.code_refactor_response:
                                with st.expander(
                                    "Refactor Code - Multiagente", expanded=True
                                ):
                                    if isinstance(
                                        result.state.code_refactor_response, str
                                    ):
                                        st.code(
                                            result.state.code_refactor_response,
                                            language="python",
                                        )

                            st.download_button(
                                label="📥 Baixar Testes Gerados",
                                data=(
                                    code_response
                                    if isinstance(code_response, str)
                                    else str(code_response)
                                ),
                                file_name="testes_multiagente.py",
                                mime="text/x-python",
                            )

                        except Exception as e:
                            st.error(f"❌ Erro na coordenação dos agentes: {str(e)}")

        # Footer
        st.markdown(
            """
            <div class="footer">
                <p><strong>LLM vs Multiagentes v2.0</strong> • Estudo Comparativo em Qualidade de Software</p>
                <p>Desenvolvido por Daniel e Ryan • © 2025 Todos os direitos reservados</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
