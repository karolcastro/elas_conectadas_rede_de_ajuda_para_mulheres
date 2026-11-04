import pytest

from elas_conectadas_mcp.services.women_training import WomenTrainingDirectory


def test_training_directory_returns_national_and_state_programs():
    result = WomenTrainingDirectory().search(uf="SP")
    ids = {item["id"] for item in result["programs"]}
    assert "sp-qualifica-ela-empreende" in ids
    assert "br-mds-educacao-financeira-mulheres" in ids
    assert all(item["free"] is True for item in result["programs"])
    assert all(item["official_source"].startswith("https://") for item in result["programs"])


def test_training_directory_filters_state_programs_and_keeps_national_programs():
    result = WomenTrainingDirectory().search(uf="MG")
    ids = {item["id"] for item in result["programs"]}
    assert "sp-qualifica-ela-empreende" not in ids
    assert "br-mds-educacao-financeira-mulheres" in ids
    assert "br-mec-mulheres-mil" in ids

    outside_offer = WomenTrainingDirectory().search(uf="RJ")
    outside_ids = {item["id"] for item in outside_offer["programs"]}
    assert "br-mec-mulheres-mil" not in outside_ids


def test_training_directory_rejects_invalid_uf():
    with pytest.raises(ValueError, match="UF"):
        WomenTrainingDirectory().search(uf="São Paulo")


def test_women_led_training_is_prioritized_and_identified():
    result = WomenTrainingDirectory().search()
    assert result["programs"][0]["provider"] == "WoMakersCode / Mais Mulheres em Tech"
    womakers = [
        item for item in result["programs"]
        if item["provider"] == "WoMakersCode / Mais Mulheres em Tech"
    ]
    assert len(womakers) == 4
    assert all(item["free"] is True for item in womakers)
    assert all(item["women_specific"] is True for item in womakers)
    assert all(item["verification_date"] == "2026-11-04" for item in womakers)


def test_women_led_national_courses_are_available_in_state_filter():
    result = WomenTrainingDirectory().search(uf="AM")
    ids = {item["id"] for item in result["programs"]}
    assert "br-womakerscode-introducao-ia" in ids
    assert "br-womakerscode-como-conseguir-emprego" in ids
    assert "br-womakerscode-lideranca-feminina" in ids



def test_programaria_sprints_are_free_national_and_prioritized():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    processes = programs["br-programaria-sprint-processos-seletivos-tech"]
    generative_ai = programs["br-programaria-sprint-ia-generativa"]
    assert processes["free"] is True
    assert processes["certificate"] is True
    assert processes["priority"] == 0
    assert "tempo indeterminado" in processes["enrollment_status"]
    assert generative_ai["free"] is True
    assert generative_ai["opportunity_type"] == "minicurso"
    assert generative_ai["priority"] == 0


def test_programaria_scholarship_waitlist_is_not_misrepresented_as_open_class():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    opportunity = programs["br-programaria-bolsas-formacao-tech-lista-interesse"]
    assert opportunity["free"] is True
    assert opportunity["opportunity_type"] == "bolsa_futura_lista_de_interesse"
    assert "Não equivale a turma com inscrições abertas" in opportunity["enrollment_status"]
    assert "não é exclusiva para elas" in opportunity["audience"]



def test_minas_programam_is_free_but_not_open_for_enrollment():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    minas = programs["br-minas-programam-introducao-programacao-proxima-turma"]
    assert minas["free"] is True
    assert minas["opportunity_type"] == "curso_proxima_turma_sem_inscricoes"
    assert "não há inscrições abertas" in minas["enrollment_status"]
    assert "não presumir oferta online" in minas["status_note"]


def test_pyladies_is_listed_as_community_with_unconfirmed_cost():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    pyladies = programs["br-pyladies-brasil-comunidade-python"]
    assert pyladies["opportunity_type"] == "comunidade"
    assert pyladies["free"] is None
    assert pyladies["women_specific"] is True
    assert "não comprova" in pyladies["coverage"]
    assert "não comprova que todos estejam realizando encontros atualmente" in pyladies["status_note"]



def test_womakerscode_cloud_course_is_free_and_online():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    cloud = programs["br-womakerscode-introducao-computacao-nuvem"]
    assert cloud["free"] is True
    assert cloud["certificate"] is True
    assert cloud["opportunity_type"] == "curso"
    assert "9,5 horas" in cloud["format"]
    assert "não informa prazo final" in cloud["enrollment_status"]


def test_pyladies_directory_does_not_claim_current_activity():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    pyladies = programs["br-pyladies-brasil-comunidade-python"]
    assert "não confirma atividade recente" in pyladies["enrollment_status"]


def test_acredita_program_prioritizes_cadunico_and_does_not_call_microcredit_free():
    programs = {item["id"]: item for item in WomenTrainingDirectory().search()["programs"]}
    acredita = programs["br-mds-acredita-primeiro-passo-inclusao-produtiva"]
    assert acredita["free"] is True
    assert acredita["priority"] == 1
    assert "CadÚnico" in acredita["audience"]
    assert "mulheres são um dos públicos prioritários" in acredita["audience"]
    assert "Microcrédito é empréstimo" in acredita["cost_note"]
    assert acredita["women_specific"] is False
