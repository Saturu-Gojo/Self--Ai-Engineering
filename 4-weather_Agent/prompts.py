from jinja2 import Environment, FileSystemLoader, select_autoescape

from schemas import tool_catalog
from config import PROMPTS_DIR


_env = Environment(
    loader=FileSystemLoader(PROMPTS_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False,
)

def render_template(name:str, **context)->str:
    return _env.get_template(name).render(**context)

def build_system_prompt(*,extra_guidance="")->str:
    return render_template(
        "system.jinja",
        tools=tool_catalog(),
        extra_guidance=extra_guidance,
    )

def build_greeting_prompt()->str:
    return render_template("greeting.jinja")