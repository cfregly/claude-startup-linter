from startup_signal_lab.router import route_claude_model
from startup_signal_lab.scoring_tools import score_startup_signal


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


def test_slop_buzzwords_cost_a_point_and_flag():
    plain = score_startup_signal("Our platform helps enterprise teams ship production agents.")
    sloppy = score_startup_signal(
        "Our revolutionary, game-changing platform seamlessly helps enterprise teams ship production agents."
    )
    assert sloppy.value_prop < plain.value_prop
    assert any("De-slop" in flag for flag in sloppy.flags)
