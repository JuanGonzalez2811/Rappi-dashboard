from groq import Groq

_client = None


def get_client():
    global _client
    if _client is None:
        _client = Groq()
    return _client


def build_context(summary: dict) -> str:
    avg_by_hour = summary.get("avg_by_hour", {})
    hour_lines = "\n".join(
        f"  {h:02d}:00 — promedio {v:,.0f}"
        for h, v in sorted(avg_by_hour.items())
    )

    avg_by_day = summary.get("avg_by_day", {})
    day_lines = "\n".join(
        f"  {d}: promedio {v:,.0f}"
        for d, v in sorted(avg_by_day.items())
    )

    avg_by_weekday = summary.get("avg_by_weekday", {})
    weekday_lines = "\n".join(
        f"  {wd}: promedio {v:,.0f}"
        for wd, v in sorted(avg_by_weekday.items())
    )

    return f"""Eres un analista de datos experto para Rappi, la super-app de delivery latinoamericana.
Tienes acceso a datos históricos de disponibilidad de tiendas: la métrica 'synthetic_monitoring_visible_stores'
mide cada 10 segundos cuántos puntos de venta son visibles/disponibles para los usuarios.

=== RESUMEN DEL DATASET ===
Rango de fechas: {summary.get('date_range', 'N/A')}
Total de puntos de datos: {summary.get('total_records', 0):,}
Días cubiertos: {summary.get('days_covered', 0)}
Promedio general: {summary.get('overall_avg', 0):,.0f}
Valor pico: {summary.get('overall_max', 0):,.0f}
Valor mínimo: {summary.get('overall_min', 0):,.0f}
Hora pico del día: {summary.get('peak_hour', 'N/A')}:00 (promedio {summary.get('peak_hour_avg', 0):,.0f})
Hora más baja del día: {summary.get('lowest_hour', 'N/A')}:00 (promedio {summary.get('lowest_hour_avg', 0):,.0f})

=== PROMEDIO POR HORA DEL DÍA (hora Colombia, UTC-5) ===
{hour_lines}

=== PROMEDIO POR DÍA CALENDARIO ===
{day_lines}

=== PROMEDIO POR DÍA DE SEMANA ===
{weekday_lines}

Responde en español de forma clara y concisa. Relaciona las respuestas con el contexto del negocio
de Rappi cuando sea relevante (demanda pico, eficiencia operacional, disponibilidad de tiendas, etc.).
Si te preguntan algo que no está cubierto en los datos, dilo claramente."""


def chat(messages: list, summary: dict) -> str:
    system_prompt = build_context(summary)
    client = get_client()

    groq_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in messages
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        max_tokens=1024,
        temperature=0.3,
    )
    return response.choices[0].message.content
