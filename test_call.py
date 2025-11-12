from services.extraction_service import extract_ticket
import json

base_input = {
    "channel": "Game Launch Issue",
    "Test Login ID": "test_user",
    "Test Login Password": "p@ssw0rd",
    "Game Launch URL": "https://casino.example/launch",
    "VPN": "vpn-prod",
    "Brand / Casino Company Name": "Example Casino Ltd",
    "Player Name": "Alice Smith",
    "Round ID": "RND-98765",
    "Game Name": "Roulette VIP",
    "Brand Name": "VIP Brand",
    "MID": "MID-55",
    "Player ID": "PID-123",
    "Event Date & Time": "2025-11-11 14:30:00",
    "Casino ID": "CAS-001",
    "Some Other Field": "ignored"
}

result = extract_ticket(base_input)
print(json.dumps(result, indent=2, ensure_ascii=False))
