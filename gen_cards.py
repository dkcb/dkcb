#!/usr/bin/env python3
"""Generate SVG project cards that mirror the dkcb.github.io hero cards."""
import html
import os

OUT = os.path.dirname(os.path.abspath(__file__))

PROJECTS = [
    dict(slug="flux", name="FLUX", tag="agentic commerce", accent="#6ee7b7",
         desc="Payments gateway where AI agents hold wallets and pay under human-set rules — built by a team in a 3-day megathon.",
         chips=["React", "TypeScript", "Vite"],
         honest="My part: the front-end (~12k LOC) · backend by teammates."),
    dict(slug="ft_transcendence", name="ft_transcendence", tag="real-time web", accent="#60a5fa",
         desc="Single-page app: live multiplayer Pong + chat, 2FA, friends, match history.",
         chips=["TypeScript", "NestJS", "React", "WebSockets"],
         honest="42 group project."),
    dict(slug="ft_linear_regression", name="ft_linear_regression", tag="ML from scratch", accent="#f0abfc",
         desc="Car-price prediction by gradient-descent linear regression — math by hand, no ML libraries.",
         chips=["Python", "gradient descent"],
         honest="Normalization + divergence/NaN safeguards."),
    dict(slug="minishell", name="minishell", tag="systems / C", accent="#fbbf24",
         desc="A Bash-like shell: tokenizing, parsing, pipes, redirections, heredocs, built-ins, signals.",
         chips=["C", "Unix", "processes"],
         honest="42 group project · fork/execve/dup2/pipe."),
    dict(slug="calculator_ts", name="calculator_ts", tag="spec-driven", accent="#34d399",
         desc="A small calculator whose logic is written test-first against a written spec.",
         chips=["TypeScript", "Jest"],
         honest="12 passing unit tests."),
    dict(slug="C-", name="C++ modules", tag="OOP fundamentals", accent="#a78bfa",
         desc="The 42 C++ modules (CPP00-06, 08-09): classes, polymorphism, operators, exceptions, STL.",
         chips=["C++98", "OOP"],
         honest="Curriculum coursework, C++98 norm."),
]

W, H = 460, 250


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return html.escape(s, quote=True)


def card(p):
    a = p["accent"]
    desc_lines = wrap(p["desc"], 42)[:3]
    chips = p["chips"]
    chip_x = 26
    chip_svg = ""
    for c in chips:
        w = 11 + len(c) * 7.0
        chip_svg += (
            f'<g><rect x="{chip_x:.0f}" y="170" width="{w:.0f}" height="22" rx="6" '
            f'fill="none" stroke="#ffffff" stroke-opacity="0.12"/>'
            f'<text x="{chip_x + w/2:.0f}" y="185" class="chip">{esc(c)}</text></g>'
        )
        chip_x += w + 8
    desc_svg = ""
    for i, ln in enumerate(desc_lines):
        desc_svg += f'<text x="26" y="{96 + i*22}" class="desc">{esc(ln)}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="{esc(p['name'])}">
  <defs>
    <radialGradient id="g" cx="18%" cy="0%" r="80%">
      <stop offset="0" stop-color="{a}" stop-opacity="0.20"/>
      <stop offset="55%" stop-color="{a}" stop-opacity="0"/>
    </radialGradient>
    <style>
      .title {{ font: 700 23px 'Segoe UI', Ubuntu, Arial, sans-serif; fill: #eef1f6; }}
      .tag   {{ font: 600 12px 'JetBrains Mono', monospace; fill: {a}; }}
      .desc  {{ font: 400 14px 'Segoe UI', Ubuntu, Arial, sans-serif; fill: #9aa3b5; }}
      .chip  {{ font: 500 11px 'JetBrains Mono', monospace; fill: #8b93a7; text-anchor: middle; }}
      .honest{{ font: italic 400 12px 'Segoe UI', Ubuntu, Arial, sans-serif; fill: #7e8799; }}
      .arrow {{ font: 600 18px 'Segoe UI', Arial, sans-serif; fill: {a}; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="#0d1017" stroke="{a}" stroke-opacity="0.28"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="url(#g)"/>
  <rect x="26" y="26" width="{12 + len(p['tag'])*7.2:.0f}" height="24" rx="12" fill="{a}" fill-opacity="0.12" stroke="{a}" stroke-opacity="0.35"/>
  <text x="{26 + (12 + len(p['tag'])*7.2)/2:.0f}" y="42" class="tag" text-anchor="middle">{esc(p['tag'])}</text>
  <text x="{W-30}" y="44" class="arrow" text-anchor="end">→<animate attributeName="opacity" values="0.6;1;0.6" dur="3s" repeatCount="indefinite"/></text>
  <text x="26" y="74" class="title">{esc(p['name'])}</text>
  {desc_svg}
  {chip_svg}
  <line x1="26" y1="210" x2="{W-26}" y2="210" stroke="{a}" stroke-opacity="0.18"/>
  <text x="26" y="230" class="honest">{esc(p['honest'])}</text>
</svg>
'''


for p in PROJECTS:
    path = os.path.join(OUT, f"assets/card-{p['slug']}.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(card(p))
    print("wrote", path)
