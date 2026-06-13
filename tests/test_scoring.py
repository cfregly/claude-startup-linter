from startup_signal_lab.growth import (
    classify_use_cases,
    growth_office_hours,
    score_growth_readiness,
)
from startup_signal_lab.router import route_claude_model
from startup_signal_lab.scoring_tools import office_hours, score_startup_signal


def test_platform_risk_flagged():
    result = score_startup_signal("We use OpenAI and Anthropic to build agents for enterprise teams.")
    assert result.platform_risk >= 7
    assert any("platform-risk" in flag for flag in result.flags)


def test_clear_value_prop_scores_higher_than_empty():
    weak = score_startup_signal("AI platform for everyone.")
    strong = score_startup_signal("We reduce debugging time by 42% for production AI support agents using privacy-safe traces and failed tool calls.")
    assert strong.overall > weak.overall


def test_router_uses_deep_model_for_high_risk_strategy():
    route = route_claude_model("multi-step agent architecture strategy", risk="high", context_tokens=20000)
    assert "opus" in route.model
    assert route.human_review is True


def test_office_hours_surfaces_ai_platform_risk_questions():
    result = office_hours("We use OpenAI and Anthropic to build agents for enterprise teams.")
    dims = {item["dimension"] for item in result["agenda"]}
    assert "platform_risk" in dims  # naming the model providers raises platform risk
    assert "closers" in dims        # closers are always on the agenda
    pr = next(i for i in result["agenda"] if i["dimension"] == "platform_risk")
    joined = " ".join(pr["questions"]).lower()
    assert ("anthropic" in joined or "openai" in joined) and ("cloud" in joined or "aws" in joined)


def test_slop_buzzwords_cost_a_point_and_flag():
    plain = score_startup_signal("Our platform helps enterprise teams ship production agents.")
    sloppy = score_startup_signal(
        "Our revolutionary, game-changing platform seamlessly helps enterprise teams ship production agents."
    )
    assert sloppy.value_prop < plain.value_prop
    assert any("De-slop" in flag for flag in sloppy.flags)


def test_growth_flags_leaky_bucket():
    # Strong relationship, no retention story: the leaky-bucket failure.
    result = score_growth_readiness(
        "We have a waitlist from our YC community and an accelerator referral, but we have not figured out what keeps users."
    )
    assert result.relationship >= 7
    assert result.retention <= 4
    assert any("Leaky bucket" in flag for flag in result.flags)


def test_growth_office_hours_targets_weakest_stage():
    result = growth_office_hours("We classify support tickets for enterprise teams.")
    stages = {item["stage"] for item in result["agenda"]}
    assert "closers" in stages
    assert result["weakest_stage"] in {"relationship", "activation", "retention"}


def test_use_case_portfolio_sequences_to_a_dot():
    # An all-agent, no-fast-payback pitch should be told to find a Dot first.
    portfolio = classify_use_cases("We are building an autonomous multi-step agent platform.")
    assert not portfolio.dot
    assert "Dot" in portfolio.advice
