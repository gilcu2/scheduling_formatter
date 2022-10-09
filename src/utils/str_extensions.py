def clean(s: str) -> str:
    lines = s.strip().split("\n")
    lines = list(map(lambda line: line.strip(), lines))
    return "\n".join(lines)


