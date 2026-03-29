"""
ET Gen AI Hackathon — AI-Native News Experience
Multi-Agent System using Claude API + FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import anthropic
import httpx
import asyncio
import json
import re
from datetime import datetime

app = FastAPI(title="ET AI News Multi-Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

# ─────────────────────────────────────────────
#  SHARED HELPER
# ─────────────────────────────────────────────

def ask_claude(system: str, user: str, max_tokens: int = 1500) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def ask_claude_json(system: str, user: str, max_tokens: int = 1500) -> dict:
    raw = ask_claude(system, user + "\n\nRespond ONLY with valid JSON. No markdown, no explanation.", max_tokens)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


# ─────────────────────────────────────────────
#  AGENT 1 — PERSONALIZATION AGENT
#  Builds user interest profile & ranks articles
# ─────────────────────────────────────────────

class PersonalizationRequest(BaseModel):
    user_profile: dict          # {name, role, interests: [], reading_history: []}
    articles: list[dict]        # [{title, summary, category, url}]

@app.post("/agent/personalize")
async def personalize_news(req: PersonalizationRequest):
    system = """You are the Personalization Agent for Economic Times.
Your job: Given a user profile and a list of articles, rank and filter the articles
that are most relevant to this specific user. Return a JSON object with:
{
  "ranked_articles": [
    {
      "title": "...",
      "summary": "...",
      "category": "...",
      "relevance_score": 0-100,
      "why_relevant": "one sentence explaining why this matters to this user",
      "reading_time_mins": number
    }
  ],
  "personalized_greeting": "A one-line greeting addressing the user by role/interest"
}"""

    user_msg = f"""
User Profile: {json.dumps(req.user_profile)}
Available Articles: {json.dumps(req.articles)}

Rank these articles for this specific user. Top 5 only.
"""
    result = ask_claude_json(system, user_msg)
    return {"agent": "PersonalizationAgent", "result": result}


# ─────────────────────────────────────────────
#  AGENT 2 — BRIEFING AGENT
#  Synthesizes multiple articles into one deep briefing
# ─────────────────────────────────────────────

class BriefingRequest(BaseModel):
    topic: str
    articles: list[dict]        # [{title, content, source, date}]
    depth: str = "standard"     # "quick" | "standard" | "deep"

@app.post("/agent/briefing")
async def create_briefing(req: BriefingRequest):
    system = """You are the News Navigator Briefing Agent for Economic Times.
Your job: Synthesize multiple articles on a topic into ONE intelligent, interactive briefing.
Return a JSON object:
{
  "headline": "Sharp, intelligent headline",
  "tldr": "2-sentence summary for someone with 30 seconds",
  "key_sections": [
    {
      "title": "Section name",
      "insight": "The key insight in 2-3 sentences",
      "significance": "Why this matters"
    }
  ],
  "key_players": [{"name": "...", "role": "...", "stance": "..."}],
  "timeline": [{"date": "...", "event": "..."}],
  "contrarian_view": "The perspective most people are missing",
  "follow_up_questions": ["Question 1?", "Question 2?", "Question 3?"],
  "sentiment": "bullish | bearish | neutral | mixed",
  "what_to_watch": "What development to track next"
}"""

    user_msg = f"""
Topic: {req.topic}
Depth: {req.depth}
Articles to synthesize: {json.dumps(req.articles)}
"""
    result = ask_claude_json(system, user_msg, max_tokens=2000)
    return {"agent": "BriefingAgent", "result": result}


# ─────────────────────────────────────────────
#  AGENT 3 — STORY ARC TRACKER
#  Builds timeline, sentiment arc, predictions
# ─────────────────────────────────────────────

class StoryArcRequest(BaseModel):
    story_name: str
    articles: list[dict]        # [{title, date, content, sentiment_hint}]

@app.post("/agent/story-arc")
async def track_story(req: StoryArcRequest):
    system = """You are the Story Arc Tracker Agent for Economic Times.
Your job: Analyze a series of articles about an ongoing story and build a complete visual narrative.
Return a JSON object:
{
  "story_title": "...",
  "story_phase": "emerging | developing | peak | resolving | resolved",
  "timeline": [
    {
      "date": "...",
      "headline": "...",
      "sentiment": "positive | negative | neutral",
      "sentiment_score": -100 to 100,
      "key_development": "..."
    }
  ],
  "key_players": [
    {"name": "...", "role": "...", "impact": "positive | negative | neutral"}
  ],
  "sentiment_arc": "Description of how sentiment has shifted over time",
  "contrarian_perspectives": ["Perspective 1", "Perspective 2"],
  "what_to_watch_next": ["Prediction 1", "Prediction 2"],
  "story_summary": "2-paragraph summary of the entire story arc"
}"""

    user_msg = f"""
Story: {req.story_name}
Articles (chronological): {json.dumps(req.articles)}
"""
    result = ask_claude_json(system, user_msg, max_tokens=2000)
    return {"agent": "StoryArcAgent", "result": result}


# ─────────────────────────────────────────────
#  AGENT 4 — VERNACULAR AGENT
#  Context-aware translation, not literal
# ─────────────────────────────────────────────

class VernacularRequest(BaseModel):
    article_title: str
    article_content: str
    target_language: str        # "hindi" | "tamil" | "telugu" | "bengali"
    user_context: str           # "farmer" | "student" | "investor" | "general"

@app.post("/agent/vernacular")
async def translate_vernacular(req: VernacularRequest):
    system = """You are the Vernacular Business News Agent for Economic Times.
Your job: Translate business news into regional languages with CULTURAL ADAPTATION,
not literal translation. Use local metaphors, analogies, and context the reader will understand.
Return a JSON object:
{
  "translated_title": "...",
  "translated_content": "...",
  "key_terms_explained": [
    {"term": "English term", "local_explanation": "Simple explanation in target language"}
  ],
  "local_analogy": "A local analogy that makes the concept clear",
  "impact_on_reader": "How this news specifically affects someone in this reader's context",
  "language": "...",
  "adaptation_notes": "Brief note on cultural adaptations made"
}"""

    user_msg = f"""
Article Title: {req.article_title}
Article Content: {req.article_content}
Target Language: {req.target_language}
Reader Context: {req.user_context}

Adapt this news culturally for a {req.user_context} reader in {req.target_language}.
"""
    result = ask_claude_json(system, user_msg, max_tokens=2000)
    return {"agent": "VernacularAgent", "result": result}


# ─────────────────────────────────────────────
#  AGENT 5 — VIDEO SCRIPT AGENT
#  Turns article into broadcast-quality script
# ─────────────────────────────────────────────

class VideoScriptRequest(BaseModel):
    article_title: str
    article_content: str
    duration_seconds: int = 90  # 60-120

@app.post("/agent/video-script")
async def generate_video_script(req: VideoScriptRequest):
    system = """You are the AI News Video Studio Agent for Economic Times.
Your job: Transform a news article into a broadcast-quality short video script (60-120 seconds).
Return a JSON object:
{
  "title": "Video title",
  "duration_seconds": number,
  "hook": "Opening line (first 5 seconds) — must grab attention immediately",
  "segments": [
    {
      "timestamp": "0:00-0:10",
      "narration": "Exact words to say",
      "visual_direction": "What to show on screen",
      "data_overlay": "Any stat or number to display (or null)"
    }
  ],
  "closing_line": "Memorable closing statement",
  "background_music_mood": "tense | upbeat | neutral | dramatic",
  "key_stats_for_animation": ["Stat 1", "Stat 2", "Stat 3"]
}"""

    user_msg = f"""
Article: {req.article_title}
Content: {req.article_content}
Target Duration: {req.duration_seconds} seconds
"""
    result = ask_claude_json(system, user_msg, max_tokens=2000)
    return {"agent": "VideoScriptAgent", "result": result}


# ─────────────────────────────────────────────
#  ORCHESTRATOR — Runs all agents for one topic
# ─────────────────────────────────────────────

class OrchestratorRequest(BaseModel):
    topic: str
    user_profile: dict
    articles: list[dict]
    target_language: Optional[str] = "hindi"

@app.post("/orchestrate")
async def orchestrate_all(req: OrchestratorRequest):
    """Master endpoint: runs Briefing + Story Arc + Vernacular in parallel"""

    briefing_req = BriefingRequest(topic=req.topic, articles=req.articles)
    story_req = StoryArcRequest(story_name=req.topic, articles=req.articles)

    # Run briefing and story arc in parallel
    briefing_task = asyncio.create_task(
        asyncio.to_thread(
            ask_claude_json,
            """You are the News Navigator Briefing Agent. Synthesize articles into a briefing.
Return JSON: {"headline":"...","tldr":"...","key_sections":[{"title":"...","insight":"...","significance":"..."}],
"follow_up_questions":["..."],"sentiment":"...","what_to_watch":"..."}""",
            f"Topic: {req.topic}\nArticles: {json.dumps(req.articles)}"
        )
    )

    story_task = asyncio.create_task(
        asyncio.to_thread(
            ask_claude_json,
            """You are the Story Arc Tracker. Build a narrative arc from articles.
Return JSON: {"story_phase":"...","timeline":[{"date":"...","headline":"...","sentiment":"...","key_development":"..."}],
"sentiment_arc":"...","what_to_watch_next":["..."],"story_summary":"..."}""",
            f"Story: {req.topic}\nArticles: {json.dumps(req.articles)}"
        )
    )

    briefing_result, story_result = await asyncio.gather(briefing_task, story_task)

    return {
        "orchestrator": "ET AI News Multi-Agent System",
        "topic": req.topic,
        "timestamp": datetime.now().isoformat(),
        "agents_run": ["BriefingAgent", "StoryArcAgent"],
        "briefing": briefing_result,
        "story_arc": story_result,
    }


# ─────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "system": "ET AI-Native News — Multi-Agent System",
        "agents": [
            "PersonalizationAgent",
            "BriefingAgent",
            "StoryArcAgent",
            "VernacularAgent",
            "VideoScriptAgent",
            "Orchestrator",
        ],
        "status": "running"
    }
