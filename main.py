from base import FtxClient

artem = FtxClient(api_key="Sx9_99kNi2vGTK3FfQXG4CJKjQAjqbiPVXcKq4DA", api_secret="0Liu7a0NKWNXToq2KAiucYyjxgVZgb9l9HQVsw-N", subaccount_name=None)

print(artem.list_futures())