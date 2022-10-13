def clean(s: str) -> str:
    lines = s.strip().split("\n")
    lines = [line.strip() for line in lines]
    return "\n".join(lines)
