from .github import github_parser

def msg_parser(service_type: str, secret: str):
    if service_type.lower() == "github":
        return github_parser(secret)
    else:
        raise ValueError(f"Unsupported Service: {service_type}")
